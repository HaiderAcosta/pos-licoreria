import { useEffect, useState } from 'react'
import api from '../services/api'
import { Search, ChevronDown, ChevronUp } from 'lucide-react'

export default function Historial() {
  const [ventas, setVentas] = useState([])
  const [loading, setLoading] = useState(true)
  const [fechaInicio, setFechaInicio] = useState('')
  const [fechaFin, setFechaFin] = useState('')
  const [expandido, setExpandido] = useState(null)

  const cargar = () => {
    setLoading(true)
    const params = new URLSearchParams()
    if (fechaInicio) params.set('fecha_inicio', fechaInicio)
    if (fechaFin) params.set('fecha_fin', fechaFin)
    api.get(`/ventas/?${params}`).then(r => setVentas(r.data)).finally(() => setLoading(false))
  }

  useEffect(() => { cargar() }, [])

  const totalGeneral = ventas.reduce((a, v) => a + v.total, 0)

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-xl font-bold text-gray-800">Historial de ventas</h1>
        <p className="text-sm text-gray-500">{ventas.length} registros — Total: ${totalGeneral.toLocaleString('es-CO')}</p>
      </div>

      <div className="flex flex-wrap gap-3 bg-white border border-gray-200 rounded-xl p-4">
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Fecha inicio</label>
          <input type="date" value={fechaInicio} onChange={e => setFechaInicio(e.target.value)}
            className="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400" />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Fecha fin</label>
          <input type="date" value={fechaFin} onChange={e => setFechaFin(e.target.value)}
            className="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400" />
        </div>
        <div className="flex items-end">
          <button onClick={cargar} className="bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition">
            Filtrar
          </button>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
        {loading
          ? <p className="text-center py-10 text-gray-400 text-sm">Cargando...</p>
          : ventas.length === 0
            ? <p className="text-center py-10 text-gray-400 text-sm">No hay ventas en este período</p>
            : ventas.map(v => (
                <div key={v.id} className="border-b border-gray-100 last:border-0">
                  <button
                    onClick={() => setExpandido(expandido === v.id ? null : v.id)}
                    className="w-full flex items-center px-4 py-3 hover:bg-gray-50 text-left gap-4"
                  >
                    <span className="text-xs text-gray-400 w-8">#{v.id}</span>
                    <span className="text-sm font-medium text-gray-700 flex-1">
                      {new Date(v.fecha).toLocaleString('es-CO', { dateStyle: 'medium', timeStyle: 'short' })}
                    </span>
                    <span className="text-xs text-gray-500">{v.cajero?.nombre}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">{v.metodo_pago}</span>
                    <span className="font-bold text-gray-800">${v.total.toLocaleString('es-CO')}</span>
                    {expandido === v.id ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
                  </button>
                  {expandido === v.id && (
                    <div className="px-8 pb-3 space-y-1">
                      {v.items.map(i => (
                        <div key={i.id} className="flex justify-between text-xs text-gray-600 py-0.5">
                          <span>{i.producto?.nombre} × {i.cantidad}</span>
                          <span>${i.subtotal.toLocaleString('es-CO')}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))
        }
      </div>
    </div>
  )
}
