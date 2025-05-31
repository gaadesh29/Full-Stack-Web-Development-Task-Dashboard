import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { LogOut, Bell, Users, Search } from 'lucide-react';

const navLinks = [
  { name: 'Home', href: '/' },
  { name: 'Portfolio', href: '/portfolio' },
  { name: 'Mutual Funds', href: '/mutual-funds' },
  { name: 'Tools', href: '/tools' },
  { name: 'Transactions', href: '/transactions' },
];

export default function TopBar() {
  const router = useRouter();

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      router.push('/login');
    }
  };

  return (
    <header className="w-full bg-[#18191C] rounded-t-2xl flex items-center justify-between px-10 py-4 shadow font-sans" style={{ minHeight: 82 }}>
      {/* Logo */}
      <div className="flex items-center mr-8">
        <svg width="32" height="32" viewBox="0 0 40 40" fill="none">
          <g>
            <circle cx="20" cy="26" r="8" fill="#1673E6"/>
            <rect x="18" y="10" width="4" height="16" fill="#1673E6"/>
            <polygon points="20,2 26,12 14,12" fill="#1673E6"/>
          </g>
        </svg>
      </div>
      {/* Navigation */}
      <nav className="flex-1 flex items-center space-x-8">
        {navLinks.map(link => (
          <Link key={link.name} href={link.href} className="relative px-2 py-1">
            <span className={`text-base transition-colors duration-150 ${router.pathname === link.href ? 'text-white font-bold' : 'text-white font-normal'}`}>
              {link.name}
            </span>
            {router.pathname === link.href && (
              <span className="absolute left-0 -bottom-1 w-full h-0.5 bg-blue-500 rounded-full"></span>
            )}
          </Link>
        ))}
      </nav>
      {/* Icons */}
      <div className="flex items-center space-x-8 ml-8">
        {/* Search with red dot */}
        <button aria-label="Search" className="relative focus:outline-none bg-transparent p-0 flex items-center justify-center">
          <Search className="w-6 h-6 text-white" strokeWidth={1.5} />
          <span className="absolute top-0 right-0 block w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        {/* Bell */}
        <button aria-label="Notifications" className="focus:outline-none bg-transparent p-0 flex items-center justify-center">
          <Bell className="w-6 h-6 text-white" strokeWidth={1.5} />
        </button>
        {/* Users */}
        <button aria-label="Users" className="focus:outline-none bg-transparent p-0 flex items-center justify-center">
          <Users className="w-6 h-6 text-white" strokeWidth={1.5} />
        </button>
        {/* Logout */}
        <button aria-label="Logout" onClick={handleLogout} className="focus:outline-none bg-transparent p-0 flex items-center justify-center">
          <LogOut className="w-6 h-6 text-white hover:text-red-500 transition" strokeWidth={1.5} />
        </button>
      </div>
    </header>
  );
}