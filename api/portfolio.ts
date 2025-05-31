// Mock implementations for dashboard API

export async function getInvestmentOverview(userId: string) {
  return [
    { isin: 'ISIN1', mutual_fund: 'ICICI Prudential Midcap Fund', amount_invested: 575000, returns_since_investment: 15.2 },
    { isin: 'ISIN2', mutual_fund: 'Axis Flexi Cap Fund', amount_invested: 500000, returns_since_investment: -5.1 }
  ];
}

export async function getSectorAllocation(mutualFundId: string) {
  return [
    { sector: 'Financial', value: 195000, percent: 34 },
    { sector: 'Technology', value: 110000, percent: 19 },
    { sector: 'Healthcare', value: 83250, percent: 14.5 },
    { sector: 'Consumer Goods', value: 55500, percent: 9.5 },
    { sector: 'Energy', value: 55500, percent: 9.5 },
    { sector: 'Other Sectors', value: 55500, percent: 9.5 }
  ];
}

export async function getStockAllocation(mutualFundId: string) {
  return [
    { stock: 'HDFC Bank', symbol: 'HDFCBANK', weight_percent: 12 },
    { stock: 'Reliance', symbol: 'RELIANCE', weight_percent: 10 },
    { stock: 'Infosys', symbol: 'INFY', weight_percent: 8 }
  ];
}

export async function getMarketCapAllocation(mutualFundId: string) {
  return {
    large_cap_percent: 60,
    mid_cap_percent: 30,
    small_cap_percent: 10
  };
}

export async function getOverlapAnalysis(mutualFundIds: string[]) {
  return {
    overlapStocks: 5,
    averageOverlap: 12.5,
    funds: mutualFundIds
  };
} 
