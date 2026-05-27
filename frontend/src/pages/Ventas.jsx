import { useEffect, useState } from 'react'
import api from '../services/api'
import { Search, Plus, Minus, Trash2, ShoppingCart, CheckCircle } from 'lucide-react'

export default function Ventas() {
  const [productos, setProductos] = useState([])
  const [carrito, setCarrito] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [metodoPago, setMetodoPago] = useState('efectivo')
  const [loading, setLoading] = useState(false)
  const [exito, setExito] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => { cargarProductos() }, [])

  const cargarProductos = () => {
    api.get('/productos/').then(r => setProductos(r.data))
  }

  const productosFiltrados = productos.filter(p =>
    p.nombre.toLowerCase().includes(busqueda.toLowerCase())
  )

  const agregarAlCarrito = (producto) => {
    if (producto.stock === 0) return
    setCarrito(prev => {
      const existing = prev.find(i => i.id === producto.id)
      if (existing) {
        if (existing.cantidad >= producto.stock) return prev
        return prev.map(i => i.id === producto.id ? { ...i, cantidad: i.cantidad + 1 } : i)
      }
      return [...prev, { ...producto, cantidad: 1 }]
    })
  }

  const cambiarCantidad = (id, delta) => {
    setCarrito(prev =>
      prev.map(i => i.id === id ? { ...i, cantidad: Math.max(1, i.cantidad + delta) } : i)
        .filter(i => i.cantidad > 0)
    )
  }

  const eliminarItem = (id) => setCarrito(prev => prev.filter(i => i.id !== id))

  const total = carrito.reduce((acc, i) => acc + i.precio_venta * i.cantidad, 0)

  const registrarVenta = async () => {
    if (carrito.length === 0) return
    setLoading(true)
    setError('')
    try {
      await api.post('/ventas/', {
        items: carrito.map(i => ({ producto_id: i.id, cantidad: i.cantidad })),
        metodo_pago: metodoPago
      })
      setCarrito([])
      setExito(true)
      cargarProductos()
      setTimeout(() => setExito(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al registrar la venta')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col lg:flex-row gap-4 h-full">
      {/* Panel izquierdo - productos */}
      <div className="flex-1 space-y-4">
        <div>
          <h1 className="text-xl font-bold text-gray-800">Punto de venta</h1>
          <p className="text-sm text-gray-500">Selecciona los productos para agregar al carrito</p>
        </div>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar producto..."
            value={busqueda}
            onChange={e => setBusqueda(e.target.value)}
            className="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 overflow-y-auto max-h-[60vh] pb-2">
          {productosFiltrados.map(p => (
            <button
              key={p.id}
              onClick={() => agregarAlCarrito(p)}
              disabled={p.stock === 0}
              className={`text-left bg-white border rounded-xl p-3 transition hover:shadow-md hover:border-amber-300
                ${p.stock === 0 ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              <div className="text-xs text-amber-600 font-medium mb-1">{p.categoria?.nombre || 'Sin categoría'}</div>
              <div className="text-sm font-semibold text-gray-800 leading-tight mb-2">{p.nombre}</div>
              <div className="flex justify-between items-center">
                <span className="text-base font-bold text-gray-900">${p.precio_venta.toLocaleString('es-CO')}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${p.stock <= p.stock_minimo ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-700'}`}>
                  {p.stock} uds.
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Panel derecho - carrito */}
      <div className="lg:w-80 bg-white border border-gray-200 rounded-xl flex flex-col">
        <div className="p-4 border-b border-gray-100 flex items-center gap-2">
          <ShoppingCart className="w-5 h-5 text-amber-500" />
          <span className="font-semibold text-gray-800">Carrito</span>
          {carrito.length > 0 && (
            <span className="ml-auto text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">
              {carrito.length} ítem{carrito.length > 1 ? 's' : ''}
            </span>
          )}
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {carrito.length === 0
            ? <p className="text-sm text-gray-400 text-center py-10">El carrito está vacío</p>
            : carrito.map(item => (
                <div key={item.id} className="flex items-center gap-2">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-700 truncate">{item.nombre}</p>
                    <p className="text-xs text-gray-500">${item.precio_venta.toLocaleString('es-CO')} c/u</p>
                  </div>
                  <div className="flex items-center gap-1">
                    <button onClick={() => cambiarCantidad(item.id, -1)} className="p-1 rounded hover:bg-gray-100">
                      <Minus className="w-3 h-3" />
                    </button>
                    <span className="text-sm font-semibold w-6 text-center">{item.cantidad}</span>
                    <button onClick={() => cambiarCantidad(item.id, 1)} className="p-1 rounded hover:bg-gray-100">
                      <Plus className="w-3 h-3" />
                    </button>
                  </div>
                  <div className="text-sm font-bold text-gray-800 w-16 text-right">
                    ${(item.precio_venta * item.cantidad).toLocaleString('es-CO')}
                  </div>
                  <button onClick={() => eliminarItem(item.id)} className="p-1 text-red-400 hover:text-red-600">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))
          }
        </div>

        <div className="p-4 border-t border-gray-100 space-y-3">
          {error && <p className="text-xs text-red-600 bg-red-50 rounded p-2">{error}</p>}
          {exito && (
            <div className="flex items-center gap-2 text-green-600 text-sm bg-green-50 rounded p-2">
              <CheckCircle className="w-4 h-4" /> Venta registrada con éxito
            </div>
          )}

          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-500">Total</span>
            <span className="text-xl font-bold text-gray-900">${total.toLocaleString('es-CO')}</span>
          </div>

          <select
            value={metodoPago}
            onChange={e => setMetodoPago(e.target.value)}
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400"
          >
            <option value="efectivo">Efectivo</option>
            <option value="tarjeta">Tarjeta</option>
            <option value="transferencia">Transferencia</option>
          </select>

          <button
            onClick={registrarVenta}
            disabled={carrito.length === 0 || loading}
            className="w-full bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-white font-semibold py-3 rounded-xl transition text-sm"
          >
            {loading ? 'Procesando...' : `Cobrar $${total.toLocaleString('es-CO')}`}
          </button>
        </div>
      </div>
    </div>
  )
}
