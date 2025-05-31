import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement, Tooltip } from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip);

export default function LineChart() {
  const [range, setRange] = React.useState('1M');
  const data = {
    labels: ["7 Feb", "12 Feb", "17 Feb", "22 Feb", "27 Feb", "4 Mar", "9 Mar"],
    datasets: [
      {
        label: 'Portfolio Value',
        data: [500000, 510000, 505000, 515000, 525000, 520000, 550000],
        fill: false,
        borderColor: '#2563eb',
        backgroundColor: '#2563eb',
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: '#ffffff',
        pointBorderColor: '#2563eb',
        pointBorderWidth: 2,
        borderWidth: 3,
      }
    ]
  };
  const options = {
    plugins: { 
      legend: { display: false },
      tooltip: {
        backgroundColor: '#222',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#444',
        borderWidth: 1,
        padding: 12,
        boxPadding: 6,
        usePointStyle: true,
        callbacks: {
          label: function(context: any) {
            return `₹${context.parsed.y.toLocaleString()}`;
          }
        }
      }
    },
    scales: {
      x: { 
        grid: { 
          color: '#333',
          drawBorder: false
        }, 
        ticks: { 
          color: '#bdbdbd', 
          font: { 
            family: 'Inter',
            size: 12
          },
          padding: 10
        },
        border: {
          display: false
        }
      },
      y: { 
        grid: { 
          color: '#333',
          drawBorder: false
        }, 
        ticks: { 
          color: '#bdbdbd', 
          font: { 
            family: 'Inter',
            size: 12
          },
          padding: 10,
          callback: function(value: any) {
            return '₹' + value.toLocaleString();
          }
        },
        border: {
          display: false
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index' as const
    },
    maintainAspectRatio: false
  };

  return (
    <div className="bg-[#181C23] p-8 rounded-[2px] border border-white/10 shadow flex flex-col gap-8 font-sans">
      <h4 className="text-white text-xl font-bold mb-4">Performance Summary</h4>
      <div className="flex flex-col md:flex-row md:items-center md:justify-start mb-4 gap-8">
        {/* Summary Card */}
        <div className="bg-[#222] rounded-[2px] px-6 py-4 flex flex-col items-start text-left border border-white/10 min-w-[180px] max-w-[220px]">
          <span className="text-white text-lg font-bold mb-1">₹5,50,000</span>
          <span className="flex items-center text-green-400 text-base font-semibold mt-1">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"><path d="M5 12l5 5L20 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
            ₹50,000&nbsp;&nbsp;|&nbsp;&nbsp;10%
          </span>
        </div>
      </div>
      <div className="w-full h-72">
        <Line data={data} options={options} />
      </div>
      <div className="flex justify-center gap-4 mt-4">
        {['1M','3M','6M','1Y','3Y','MAX'].map(opt => (
          <button
            key={opt}
            onClick={() => setRange(opt)}
            className={`px-6 py-2 rounded-full font-semibold text-base transition-colors duration-150 shadow-sm
              ${range === opt ? 'bg-blue-600 text-white' : 'bg-[#222] text-gray-300 hover:bg-blue-200'}`}
          >
            {opt}
          </button>
        ))}
      </div>
    </div>
  );
}