import { useEffect, useState } from 'react'
import api from '../services/api'
import { TrendingUp, ShoppingBag, AlertTriangle, Package } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 flex items-center gap-4">
      <div className={`p-3 rounded-xl ${color}`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
      <div>
        <p className="text-xs text-gray-500 uppercase tracking-wide">{label}</p>
        <p className="text-2xl font-bold text-gray-800">{value}</p>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [stockBajo, setStockBajo] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/reportes/dashboard'),
      api.get('/productos/stock-bajo')
    ]).then(([res, res2]) => {
      setData(res.data)
      setStockBajo(res2.data)
    }).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="flex items-center justify-center h-64 text-gray-400">Cargando...</div>

  const chartData = data?.top_productos?.map(p => ({ name: p.nombre.split(' ').slice(0, 2).join(' '), vendidos: p.total_vendido })) || []

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-sm text-gray-500">Resumen de hoy — {new Date().toLocaleDateString('es-CO', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <StatCard icon={TrendingUp} label="Ventas hoy" value={`$${(data?.ventas_hoy || 0).toLocaleString('es-CO')}`} color="bg-green-500" />
        <StatCard icon={ShoppingBag} label="Transacciones" value={data?.transacciones_hoy || 0} color="bg-blue-500" />
        <StatCard icon={AlertTriangle} label="Stock bajo" value={data?.productos_stock_bajo || 0} color="bg-red-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="font-semibold text-gray-800 mb-4 text-sm">Top 5 productos más vendidos</h2>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={chartData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="vendidos" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="text-sm text-gray-400 py-8 text-center">Sin ventas registradas aún</p>}
        </div>

        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="font-semibold text-gray-800 mb-4 text-sm flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-red-500" />
            Productos con stock bajo
          </h2>
          {stockBajo.length === 0
            ? <p className="text-sm text-gray-400 py-8 text-center">Todo el inventario está bien</p>
            : <div className="space-y-2">
                {stockBajo.map(p => (
                  <div key={p.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                    <span className="text-sm text-gray-700">{p.nombre}</span>
                    <span className="text-xs font-semibold bg-red-100 text-red-700 px-2 py-0.5 rounded-full">
                      {p.stock} uds.
                    </span>
                  </div>
                ))}
              </div>
          }
        </div>
      </div>
    </div>
  )
}
