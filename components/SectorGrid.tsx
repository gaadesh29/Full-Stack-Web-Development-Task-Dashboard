import React from 'react';

interface Sector {
  name: string;
  amount: number;
  percentage: number;
  color: string;
}

interface SectorGridProps {
  data: Sector[];
}

export default function SectorGrid({ data }: SectorGridProps) {
  // Figma-inspired color palette
  const colorMap: Record<string, string> = {
    Financial: 'bg-[#B6C6D7]',
    Healthcare: 'bg-[#C3C9DF]',
    Technology: 'bg-[#D1CBEA]',
    'Consumer Goods': 'bg-[#E3DDF2]',
    Energy: 'bg-[#E3DDF2]',
    'Other Sectors': 'bg-[#F5F5F7]'
  };
  const textColorMap: Record<string, string> = {
    Financial: 'text-[#22223B]',
    Healthcare: 'text-[#22223B]',
    Technology: 'text-[#22223B]',
    'Consumer Goods': 'text-[#22223B]',
    Energy: 'text-[#22223B]',
    'Other Sectors': 'text-[#22223B]'
  };

  return (
    <div className="bg-[#181C23] p-6 rounded-2xl">
      <h4 className="text-white text-base font-bold mb-4">Sector Allocation</h4>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* First row: Financial (2 cols), Healthcare (2 cols) */}
        <div className={`col-span-2 row-span-1 rounded-xl p-6 flex flex-col justify-between ${colorMap['Financial']} ${textColorMap['Financial']}`}>
          <div>
            <div className="text-base font-semibold mb-1">Financial</div>
            <div className="text-sm mb-2">₹1,95,000</div>
          </div>
          <div className="text-2xl font-bold">34%</div>
        </div>
        <div className={`col-span-2 row-span-1 rounded-xl p-6 flex flex-col justify-between ${colorMap['Healthcare']} ${textColorMap['Healthcare']}`}>
          <div>
            <div className="text-base font-semibold mb-1">Healthcare</div>
            <div className="text-sm mb-2">₹83,250</div>
          </div>
          <div className="text-2xl font-bold">14.5%</div>
        </div>
        {/* Second row: Technology, Consumer Goods, Energy, Other Sectors */}
        <div className={`col-span-1 row-span-1 rounded-xl p-6 flex flex-col justify-between ${colorMap['Technology']} ${textColorMap['Technology']}`}>
          <div>
            <div className="text-base font-semibold mb-1">Technology</div>
            <div className="text-sm mb-2">₹1,11,000</div>
          </div>
          <div className="text-2xl font-bold">19%</div>
        </div>
        <div className={`col-span-1 row-span-1 rounded-xl p-6 flex flex-col justify-between ${colorMap['Consumer Goods']} ${textColorMap['Consumer Goods']}`}>
          <div>
            <div className="text-base font-semibold mb-1">Consumer Goods</div>
            <div className="text-sm mb-2">₹55,500</div>
          </div>
          <div className="text-2xl font-bold">9.5%</div>
        </div>
        <div className={`col-span-1 row-span-1 rounded-xl p-6 flex flex-col justify-between ${colorMap['Energy']} ${textColorMap['Energy']}`}>
          <div>
            <div className="text-base font-semibold mb-1">Energy</div>
            <div className="text-sm mb-2">₹55,500</div>
          </div>
          <div className="text-2xl font-bold">9.5%</div>
        </div>
        <div className={`col-span-1 row-span-1 rounded-xl p-6 flex flex-col justify-between ${colorMap['Other Sectors']} ${textColorMap['Other Sectors']}`}>
          <div>
            <div className="text-base font-semibold mb-1">Other Sectors</div>
            <div className="text-sm mb-2">₹55,500</div>
          </div>
          <div className="text-2xl font-bold">9.5%</div>
        </div>
      </div>
    </div>
  );
}