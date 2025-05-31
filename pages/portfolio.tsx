import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import * as jwt_decode from 'jwt-decode';
import Sidebar from '../components/Sidebar';
import TopBar from '../components/TopBar';
import InvestmentSummary from '../components/InvestmentSummary';
import LineChart from '../components/LineChart';
import SectorGrid from '../components/SectorGrid';
import SankeyChart from '../components/SankeyChart';
import { useQuery } from '@tanstack/react-query';
import { getInvestmentOverview, getSectorAllocation, getStockAllocation, getMarketCapAllocation, getOverlapAnalysis } from '../api/portfolio';
import StockGrid from '../components/StockGrid';
import MarketCapChart from '../components/MarketCapChart';

function getUserIdFromToken() {
  if (typeof window === 'undefined') return null;
  const token = localStorage.getItem('token');
  if (!token) return null;
  try {
    const decoded: any = jwt_decode.jwtDecode(token);
    return decoded.sub;
  } catch {
    return null;
  }
}

export default function Portfolio() {
  const [activeTab, setActiveTab] = useState("metrics");
  const router = useRouter();

  useEffect(() => {
    // if (typeof window !== 'undefined' && !localStorage.getItem('token')) {
    //   router.push('/login');
    // }
  }, [router]);

  const userId = getUserIdFromToken();
  // TODO: Replace with actual mutual fund ID (e.g., from selected fund in UI)
  const mutualFundId = 'YOUR_MUTUAL_FUND_ID';
  const mutualFundIds = ['FUND_ID_1', 'FUND_ID_2'];

  const { data, isLoading, error } = useQuery({
    queryKey: ['investmentOverview', userId],
    queryFn: () => getInvestmentOverview(userId),
    enabled: !!userId
  });

  const { data: sectorAllocationData, isLoading: sectorAllocationLoading, error: sectorAllocationError } = useQuery({
    queryKey: ['sectorAllocation', mutualFundId],
    queryFn: () => getSectorAllocation(mutualFundId)
  });

  const { data: stockAllocation, isLoading: stockLoading, error: stockError } = useQuery({
    queryKey: ['stockAllocation', mutualFundId],
    queryFn: () => getStockAllocation(mutualFundId)
  });

  const { data: marketCapAllocation, isLoading: marketCapLoading, error: marketCapError } = useQuery({
    queryKey: ['marketCapAllocation', mutualFundId],
    queryFn: () => getMarketCapAllocation(mutualFundId)
  });

  const { data: overlapData, isLoading: overlapLoading, error: overlapError } = useQuery({
    queryKey: ['overlapAnalysis', mutualFundIds],
    queryFn: () => getOverlapAnalysis(mutualFundIds)
  });

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };

  if (isLoading || sectorAllocationLoading || stockLoading || marketCapLoading || overlapLoading) return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900">
      <div className="text-white text-xl">Loading your portfolio data...</div>
    </div>
  );
  
  if (error || sectorAllocationError || stockError || marketCapError || overlapError) return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900">
      <div className="text-white text-xl">
        <p>Error loading portfolio data</p>
        <p className="text-sm text-gray-400 mt-2">Please try refreshing the page</p>
      </div>
    </div>
  );

  return (
    <div className="flex bg-gray-900 min-h-screen text-white">
      <Sidebar />
      <div className="flex flex-col flex-grow">
        <TopBar />
        <button 
          onClick={handleLogout} 
          className="absolute top-4 right-4 bg-red-600 hover:bg-red-700 px-6 py-2 rounded-full font-bold transition-colors duration-200 shadow-sm"
        >
          Logout
        </button>
        <main className="p-8 md:p-12 space-y-8 font-sans">
          {/* Greeting and subtitle */}
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-white">Good morning, Yashna!</h2>
            <p className="text-gray-400 text-lg mt-2">Evaluate Your Investment Performance</p>
          </div>

          {/* Summary cards row */}
          <div className="flex flex-col sm:flex-row gap-6 mb-8">
            <InvestmentSummary 
              title="Current Investment Value" 
              value="₹5,75,000" 
              subtitle={<span className="flex items-center"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="mr-1"><path d="M8 12l4-4 4 4" stroke="#4ADE80" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M12 20V8" stroke="#4ADE80" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>+0.6% 1D Return</span>} 
              active
              positive
            />
            <InvestmentSummary 
              title="Initial Investment Value" 
              value="₹5,00,000" 
              subtitle={<span className="flex items-center"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="mr-1"><path d="M8 12l4-4 4 4" stroke="#4ADE80" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M12 20V8" stroke="#4ADE80" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>+15% Inception</span>} 
              positive
            />
            <InvestmentSummary 
              title="Best Performing Scheme" 
              value="ICICI Prudential Midcap Fund" 
              subtitle={<span className="flex items-center"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="mr-1"><path d="M8 12l4-4 4 4" stroke="#4ADE80" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M12 20V8" stroke="#4ADE80" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>+19% Inception</span>} 
              positive
            />
            <InvestmentSummary 
              title="Worst Performing Scheme" 
              value="Axis Flexi Cap Fund" 
              subtitle={<span className="flex items-center"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="mr-1"><path d="M16 12l-4 4-4-4" stroke="#F87171" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M12 4v12" stroke="#F87171" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>-5% Inception</span>} 
              positive={false}
            />
          </div>

          {/* Tabs section refined for Figma accuracy */}
          <div className="w-full flex flex-col font-sans">
            <div className="flex space-x-12 border-b border-white/10 w-full mb-8">
              <button
                onClick={() => setActiveTab("metrics")}
                className={`relative px-2 py-2 text-lg transition-colors duration-200 focus:outline-none
                  ${activeTab === "metrics" ? "text-white font-bold" : "text-white font-normal"}`}
                style={{ minWidth: '180px', textAlign: 'left' }}
              >
                Performance Metrics
                {activeTab === "metrics" && (
                  <span className="absolute left-0 -bottom-1 w-9/12 h-0.5 bg-blue-600 rounded-full"></span>
                )}
              </button>
              <button
                onClick={() => setActiveTab("composition")}
                className={`relative px-2 py-2 text-lg transition-colors duration-200 focus:outline-none
                  ${activeTab === "composition" ? "text-white font-bold" : "text-white font-normal"}`}
                style={{ minWidth: '220px', textAlign: 'left' }}
              >
                Portfolio Composition
                {activeTab === "composition" && (
                  <span className="absolute left-0 -bottom-1 w-9/12 h-0.5 bg-blue-600 rounded-full"></span>
                )}
              </button>
            </div>
          </div>

          <div className="mt-12">
            {activeTab === "metrics" && (
              <>
                <h2 className="text-3xl font-extrabold text-white mb-8">Performance Metrics</h2>
                <LineChart />
              </>
            )}
            {activeTab === "composition" && (
              <div className="space-y-12">
                <h2 className="text-3xl font-extrabold text-white mb-8">Portfolio Composition</h2>
                <SectorGrid data={sectorAllocationData.map(sector => ({
                  name: sector.sector,
                  amount: sector.value,
                  percentage: sector.percent,
                  color: sector.sector === 'Financial' ? 'blue' : sector.sector === 'Healthcare' ? 'pink' : sector.sector === 'Technology' ? 'purple' : sector.sector === 'Consumer Goods' ? 'yellow' : sector.sector === 'Energy' ? 'red' : 'gray'
                }))} />
                <div>
                  <h2 className="text-3xl font-extrabold text-white mb-8">Overlap Analysis</h2>
                  <SankeyChart />
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}