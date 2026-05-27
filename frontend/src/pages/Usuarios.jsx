import { useEffect, useState } from 'react'
import api from '../services/api'
import { Plus, UserX, X } from 'lucide-react'

export default function Usuarios() {
  const [usuarios, setUsuarios] = useState([])
  const [modal, setModal] = useState(false)
  const [form, setForm] = useState({ nombre: '', email: '', password: '', rol: 'cajero' })
  const [loading, setLoading] = useState(false)

  useEffect(() => { cargar() }, [])
  const cargar = () => api.get('/usuarios/').then(r => setUsuarios(r.data))

  const crear = async () => {
    setLoading(true)
    try {
      await api.post('/usuarios/', form)
      setModal(false)
      setForm({ nombre: '', email: '', password: '', rol: 'cajero' })
      cargar()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error')
    } finally { setLoading(false) }
  }

  const desactivar = async (id) => {
    if (!confirm('¿Desactivar este usuario?')) return
    await api.put(`/usuarios/${id}/desactivar`)
    cargar()
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-800">Usuarios</h1>
          <p className="text-sm text-gray-500">{usuarios.length} usuarios registrados</p>
        </div>
        <button onClick={() => setModal(true)} className="flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white text-sm font-semibold px-4 py-2.5 rounded-lg transition">
          <Plus className="w-4 h-4" /> Nuevo usuario
        </button>
      </div>

      <div className="grid gap-3">
        {usuarios.map(u => (
          <div key={u.id} className="bg-white border border-gray-200 rounded-xl px-5 py-4 flex items-center gap-4">
            <div className="w-10 h-10 rounded-full bg-amber-100 flex items-center justify-center text-amber-700 font-bold text-sm">
              {u.nombre.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-gray-800 text-sm">{u.nombre}</p>
              <p className="text-xs text-gray-500">{u.email}</p>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${u.rol === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'}`}>
              {u.rol}
            </span>
            <span className={`text-xs px-2.5 py-1 rounded-full ${u.activo ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
              {u.activo ? 'Activo' : 'Inactivo'}
            </span>
            {u.activo && (
              <button onClick={() => desactivar(u.id)} className="p-1.5 text-red-400 hover:bg-red-50 rounded-lg">
                <UserX className="w-4 h-4" />
              </button>
            )}
          </div>
        ))}
      </div>

      {modal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6">
            <div className="flex items-center justify-between mb-5">
              <h2 className="font-bold text-gray-800">Nuevo usuario</h2>
              <button onClick={() => setModal(false)}><X className="w-5 h-5 text-gray-400" /></button>
            </div>
            <div className="space-y-3">
              {[['nombre', 'Nombre completo', 'text'], ['email', 'Correo electrónico', 'email'], ['password', 'Contraseña', 'password']].map(([key, label, type]) => (
                <div key={key}>
                  <label className="block text-xs font-medium text-gray-600 mb-1">{label}</label>
                  <input type={type} value={form[key]} onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}
                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400" />
                </div>
              ))}
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Rol</label>
                <select value={form.rol} onChange={e => setForm(f => ({ ...f, rol: e.target.value }))}
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400">
                  <option value="cajero">Cajero</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={() => setModal(false)} className="flex-1 border border-gray-200 rounded-lg py-2.5 text-sm hover:bg-gray-50">Cancelar</button>
              <button onClick={crear} disabled={loading} className="flex-1 bg-amber-500 hover:bg-amber-600 text-white rounded-lg py-2.5 text-sm font-semibold disabled:opacity-50">
                {loading ? 'Creando...' : 'Crear usuario'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
