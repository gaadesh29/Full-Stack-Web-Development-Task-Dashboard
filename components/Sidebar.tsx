import React from 'react';

export default function Sidebar() {
  return (
    <aside className="w-56 h-screen bg-[#1A1A1A] text-white flex flex-col pt-8 pb-4 px-6 rounded-bl-2xl font-sans">
      {/* Logo */}
      <div className="flex items-center justify-center mb-10">
        <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
          <g>
            <circle cx="20" cy="26" r="8" fill="#1673E6"/>
            <rect x="18" y="10" width="4" height="16" fill="#1673E6"/>
            <polygon points="20,2 26,12 14,12" fill="#1673E6"/>
          </g>
        </svg>
      </div>
      {/* Active Section and Menu */}
      <div>
        <div className="bg-[#444444] rounded-lg px-4 py-2 font-bold text-white text-sm mb-8">PHA</div>
        <nav className="flex flex-col gap-8">
          <span className="text-gray-300 text-base font-normal cursor-pointer hover:text-white transition">Fund Analysis</span>
          <span className="text-gray-300 text-base font-normal cursor-pointer hover:text-white transition">Holdings</span>
          <span className="text-gray-300 text-base font-normal cursor-pointer hover:text-white transition">Transactions</span>
        </nav>
      </div>
    </aside>
  );
}