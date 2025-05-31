import React from 'react';

interface MarketCapData {
  large_cap_percent: number;
  mid_cap_percent: number;
  small_cap_percent: number;
}

export default function MarketCapChart({ data }: { data: MarketCapData }) {
  if (!data) return null;

  const getColor = (type: string) => {
    switch (type) {
      case 'large':
        return 'bg-blue-100 text-blue-700';
      case 'mid':
        return 'bg-purple-100 text-purple-700';
      case 'small':
        return 'bg-pink-100 text-pink-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const getBarColor = (type: string) => {
    switch (type) {
      case 'large':
        return 'bg-blue-500';
      case 'mid':
        return 'bg-purple-500';
      case 'small':
        return 'bg-pink-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="bg-white rounded-3xl p-8 shadow-lg">
      <h4 className="text-gray-800 mb-6 text-xl font-bold">Market Cap Allocation</h4>
      <div className="space-y-6">
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-600 font-medium">Large Cap</span>
            <span className="text-gray-800 font-bold">{data.large_cap_percent}%</span>
          </div>
          <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div 
              className={`h-full ${getBarColor('large')} rounded-full transition-all duration-500`}
              style={{ width: `${data.large_cap_percent}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-600 font-medium">Mid Cap</span>
            <span className="text-gray-800 font-bold">{data.mid_cap_percent}%</span>
          </div>
          <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div 
              className={`h-full ${getBarColor('mid')} rounded-full transition-all duration-500`}
              style={{ width: `${data.mid_cap_percent}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-600 font-medium">Small Cap</span>
            <span className="text-gray-800 font-bold">{data.small_cap_percent}%</span>
          </div>
          <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div 
              className={`h-full ${getBarColor('small')} rounded-full transition-all duration-500`}
              style={{ width: `${data.small_cap_percent}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
} 