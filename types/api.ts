export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

export interface Portfolio {
  id: string;
  user_id: string;
  name: string;
  total_value: number;
  created_at: string;
  updated_at: string;
}

export interface Investment {
  id: string;
  portfolio_id: string;
  fund_id: string;
  amount: number;
  units: number;
  purchase_date: string;
  current_value: number;
}

export interface MutualFund {
  id: string;
  name: string;
  category: string;
  nav: number;
  return_1d: number;
  return_1w: number;
  return_1m: number;
  return_1y: number;
}

export interface Sector {
  id: string;
  name: string;
  allocation: number;
}

export interface Stock {
  id: string;
  name: string;
  symbol: string;
  sector_id: string;
  price: number;
  change_percentage: number;
}

export interface Transaction {
  id: string;
  portfolio_id: string;
  fund_id: string;
  type: 'BUY' | 'SELL';
  units: number;
  amount: number;
  date: string;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
} 