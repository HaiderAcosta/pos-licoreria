import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import {
  LayoutDashboard, ShoppingCart, Package, History,
  Users, LogOut, Wine, Menu, X
} from 'lucide-react'
import { useState } from 'react'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, admin: true },
  { to: '/ventas', label: 'Punto de venta', icon: ShoppingCart, admin: false },
  { to: '/inventario', label: 'Inventario', icon: Package, admin: true },
  { to: '/historial', label: 'Historial ventas', icon: History, admin: true },
  { to: '/usuarios', label: 'Usuarios', icon: Users, admin: true },
]

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)

  const handleLogout = () => { logout(); navigate('/login') }
  const items = navItems.filter(i => !i.admin || user?.rol === 'admin')

  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 z-40 w-56 bg-gray-900 text-white flex flex-col transition-transform duration-200
        ${open ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 lg:static lg:flex`}>
        <div className="flex items-center gap-2 px-5 py-5 border-b border-gray-700">
          <Wine className="w-6 h-6 text-amber-400" />
          <span className="font-bold text-sm leading-tight">POS Licorería<br /><span className="font-normal text-gray-400 text-xs">Fusagasugá</span></span>
        </div>
        <nav className="flex-1 px-3 py-4 space-y-1">
          {items.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition
                ${isActive ? 'bg-amber-500 text-white' : 'text-gray-300 hover:bg-gray-800'}`
              }
            >
              <Icon className="w-4 h-4" />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-gray-700">
          <div className="text-xs text-gray-400 mb-1">{user?.nombre}</div>
          <div className="text-xs text-amber-400 mb-3 capitalize">{user?.rol}</div>
          <button onClick={handleLogout} className="flex items-center gap-2 text-sm text-gray-300 hover:text-white transition">
            <LogOut className="w-4 h-4" /> Cerrar sesión
          </button>
        </div>
      </aside>

      {/* Overlay mobile */}
      {open && <div className="fixed inset-0 z-30 bg-black/50 lg:hidden" onClick={() => setOpen(false)} />}

      <div className="flex-1 flex flex-col min-w-0">
        <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-3 lg:hidden">
          <button onClick={() => setOpen(true)} className="p-1"><Menu className="w-5 h-5" /></button>
          <span className="font-semibold text-sm">POS Licorería</span>
        </header>
        <main className="flex-1 p-4 lg:p-6 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
