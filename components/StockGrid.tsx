import React from 'react';

export default function StockGrid({ data }: { data: any }) {
  if (!data) return null;
  return (
    <div className="bg-[#181C23] rounded-3xl p-8 mt-4 shadow-[0_4px_24px_0_rgba(0,0,0,0.18)] transition-all duration-200 hover:shadow-2xl hover:scale-[1.02]">
      <h4 className="text-white mb-2 text-lg font-semibold">Stock Allocation</h4>
      <ul className="space-y-1">
        {data.map((item: any) => (
          <li key={item.symbol} className="text-gray-200">
            {item.stock} <span className="text-gray-400">({item.symbol})</span>: <span className="font-medium">{item.weight_percent}%</span>
          </li>
        ))}
      </ul>
    </div>
  );
} 