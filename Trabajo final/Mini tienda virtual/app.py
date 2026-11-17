import json
from pathlib import Path
from urllib.parse import quote

import streamlit as st


st.set_page_config(
    page_title="Moda Urbana",
    page_icon="👕",
    layout="wide",
)

PRODUCTOS = [
    {"id": 1, "nombre": "Camiseta básica", "categoria": "Camisetas", "precio": 45000, "emoji": "👕", "color": "#7EA6F7", "stock": 12},
    {"id": 2, "nombre": "Camisa oversize", "categoria": "Camisetas", "precio": 68000, "emoji": "👔", "color": "#A9C9C5", "stock": 8},
    {"id": 3, "nombre": "Chaqueta urbana", "categoria": "Chaquetas", "precio": 135000, "emoji": "🧥", "color": "#A8A4CE", "stock": 5},
    {"id": 4, "nombre": "Buzo con capota", "categoria": "Sudaderas", "precio": 82000, "emoji": "🧥", "color": "#F2C14E", "stock": 10},
    {"id": 5, "nombre": "Pantalón casual", "categoria": "Pantalones", "precio": 95000, "emoji": "👖", "color": "#7FA7D7", "stock": 9},
    {"id": 6, "nombre": "Vestido elegante", "categoria": "Vestidos", "precio": 110000, "emoji": "👗", "color": "#E7A8B8", "stock": 6},
    {"id": 7, "nombre": "Falda moderna", "categoria": "Faldas", "precio": 58000, "emoji": "👗", "color": "#D8A7CB", "stock": 7},
    {"id": 8, "nombre": "Tenis deportivos", "categoria": "Calzado", "precio": 120000, "emoji": "👟", "color": "#D5D7D8", "stock": 11},
]

STOCK_PATH = Path(__file__).with_name("stock.json")


def cargar_stock():
    if STOCK_PATH.exists():
        try:
            guardado = json.loads(STOCK_PATH.read_text(encoding="utf-8"))
            for producto in PRODUCTOS:
                producto["stock"] = int(guardado.get(str(producto["id"]), producto["stock"]))
        except (json.JSONDecodeError, OSError, ValueError, TypeError):
            st.warning("No se pudo leer el archivo de stock. Se usaron las unidades iniciales.")


def guardar_stock():
    datos = {str(producto["id"]): producto["stock"] for producto in PRODUCTOS}
    STOCK_PATH.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")


def stock_disponible(producto):
    return producto["stock"] - st.session_state.carrito.get(producto["id"], 0)


cargar_stock()


def pesos(valor):
    return f"${valor:,.0f}".replace(",", ".")


if "carrito" not in st.session_state:
    st.session_state.carrito = {}
if "pedido_confirmado" not in st.session_state:
    st.session_state.pedido_confirmado = False
if "mensaje_whatsapp" not in st.session_state:
    st.session_state.mensaje_whatsapp = ""


st.title("Moda Urbana")
st.caption("Prendas cómodas, modernas y para todos los días")


# Filtros
st.sidebar.title("Tienda")
st.sidebar.subheader("Contacto")
numero_whatsapp = st.sidebar.text_input(
    "WhatsApp de la tienda",
    value="573177055617",
    help="Escribe el número con código de país, sin espacios ni signos. Ejemplo: 573001234567.",
)
busqueda = st.sidebar.text_input("Buscar prenda", placeholder="Ej: camiseta")
categorias = ["Todas"] + sorted({producto["categoria"] for producto in PRODUCTOS})
categoria = st.sidebar.selectbox("Categoría", categorias)
orden = st.sidebar.selectbox(
    "Ordenar por",
    ["Destacados", "Precio: menor a mayor", "Precio: mayor a menor"],
)

productos = PRODUCTOS
if categoria != "Todas":
    productos = [producto for producto in productos if producto["categoria"] == categoria]
if busqueda:
    productos = [
        producto for producto in productos
        if busqueda.lower() in producto["nombre"].lower()
    ]
if orden == "Precio: menor a mayor":
    productos = sorted(productos, key=lambda producto: producto["precio"])
elif orden == "Precio: mayor a menor":
    productos = sorted(productos, key=lambda producto: producto["precio"], reverse=True)


# Catálogo
st.subheader("Catálogo de ropa")
if not productos:
    st.info("No encontramos prendas con esos filtros.")
else:
    columnas_por_fila = 3
    for inicio in range(0, len(productos), columnas_por_fila):
        columnas = st.columns(columnas_por_fila)
        for columna, producto in zip(columnas, productos[inicio:inicio + columnas_por_fila]):
            with columna:
                st.markdown(
                    f"""
                    <div style="background:{producto["color"]};border-radius:16px;
                    height:170px;display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:86px">{producto["emoji"]}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(f"### {producto['nombre']}")
                st.write(f"**{pesos(producto['precio'])}**  ·  {producto['categoria']}")

                cantidad_en_carrito = st.session_state.carrito.get(producto["id"], 0)
                disponible = stock_disponible(producto)
                st.caption(f"{disponible} unidades disponibles")

                if st.button(
                    "Agregar al carrito",
                    key=f"agregar_{producto['id']}",
                    disabled=disponible <= 0,
                    use_container_width=True,
                ):
                    st.session_state.carrito[producto["id"]] = cantidad_en_carrito + 1
                    st.session_state.pedido_confirmado = False
                    st.rerun()


# Carrito
st.divider()
st.subheader("🛒 Tu carrito")

if not st.session_state.carrito:
    st.info("Tu carrito está vacío. Agrega una prenda para comenzar.")
else:
    total = 0

    for producto_id, cantidad in list(st.session_state.carrito.items()):
        producto = next(item for item in PRODUCTOS if item["id"] == producto_id)
        subtotal = producto["precio"] * cantidad
        total += subtotal

        col_producto, col_cantidad, col_subtotal, col_eliminar = st.columns([4, 2, 2, 1])
        with col_producto:
            st.write(f"{producto['emoji']} **{producto['nombre']}**")
        with col_cantidad:
            nueva_cantidad = st.number_input(
                "Cantidad",
                min_value=1,
                max_value=producto["stock"],
                value=cantidad,
                key=f"cantidad_{producto_id}",
                label_visibility="collapsed",
            )
            if nueva_cantidad != cantidad:
                st.session_state.carrito[producto_id] = nueva_cantidad
                st.rerun()
        with col_subtotal:
            st.write(pesos(subtotal))
        with col_eliminar:
            if st.button("✕", key=f"eliminar_{producto_id}", help="Eliminar producto"):
                del st.session_state.carrito[producto_id]
                st.rerun()

    st.markdown(f"## Total: {pesos(total)}")

    col_pagar, col_vaciar = st.columns(2)
    with col_pagar:
        if st.button("Confirmar pedido", type="primary", use_container_width=True):
            pedido = []
            pedido_valido = True

            for producto_id, cantidad in st.session_state.carrito.items():
                producto = next(item for item in PRODUCTOS if item["id"] == producto_id)
                if cantidad > producto["stock"]:
                    pedido_valido = False
                    break
                pedido.append(f"{cantidad} x {producto['nombre']} - {pesos(producto['precio'] * cantidad)}")

            if pedido_valido:
                for producto_id, cantidad in st.session_state.carrito.items():
                    producto = next(item for item in PRODUCTOS if item["id"] == producto_id)
                    producto["stock"] -= cantidad
                guardar_stock()

                mensaje = "Hola, quiero confirmar el siguiente pedido:\n\n"
                mensaje += "\n".join(pedido)
                mensaje += f"\n\nTotal: {pesos(total)}\n¿Podemos acordar la forma de pago?"
                st.session_state.mensaje_whatsapp = mensaje
                st.session_state.pedido_confirmado = True
                st.session_state.carrito = {}
            else:
                st.error("No hay stock suficiente para completar el pedido.")
            st.rerun()
    with col_vaciar:
        if st.button("Vaciar carrito", use_container_width=True):
            st.session_state.carrito = {}
            st.rerun()

if st.session_state.pedido_confirmado:
    st.success("¡Pedido confirmado! Gracias por comprar en Moda Urbana.")
    if numero_whatsapp and st.session_state.mensaje_whatsapp:
        whatsapp_url = (
            f"https://wa.me/{numero_whatsapp}?text={quote(st.session_state.mensaje_whatsapp)}"
        )
        st.link_button("Enviar pedido por WhatsApp", whatsapp_url)
