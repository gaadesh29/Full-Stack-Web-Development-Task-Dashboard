import React, { ReactNode } from 'react';

interface SummaryProps {
  title: string;
  value: string;
  subtitle?: ReactNode;
  active?: boolean;
  positive?: boolean;
}

export default function InvestmentSummary({ title, value, subtitle, active, positive }: SummaryProps) {
  return (
    <div className={`bg-[#11263C] rounded-xl px-4 py-3 flex flex-col min-w-[250px] border-l-2 relative ${active ? 'border-l-[#2D9CDB]' : 'border-l-[#183153]'} border border-[#183153]`}>  
      {/* Top row: subtitle right */}
      <div className="flex justify-between items-start mb-2">
        <div className="flex-1">
          <div className="text-white text-base font-normal leading-tight">{title}</div>
        </div>
        {subtitle && (
          <div className={`text-xs font-medium ${positive === false ? 'text-red-400' : 'text-green-400'} ml-2 whitespace-nowrap flex items-center`}>{subtitle}</div>
        )}
      </div>
      {/* Value bottom left */}
      <div className="text-white text-xl font-bold mt-1">{value}</div>
    </div>
  );
}