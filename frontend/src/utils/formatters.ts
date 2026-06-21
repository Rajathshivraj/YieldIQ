// Utility helpers

export const formatCurrency = (value: number, compact = false): string => {
  if (compact) {
    if (value >= 1_00_00_000) return `₹${(value / 1_00_00_000).toFixed(2)}Cr`;
    if (value >= 1_00_000) return `₹${(value / 1_00_000).toFixed(2)}L`;
    if (value >= 1_000) return `₹${(value / 1_000).toFixed(1)}K`;
    return `₹${value.toFixed(0)}`;
  }
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(value);
};

export const formatPercent = (value: number, decimals = 1): string =>
  `${value >= 0 ? '+' : ''}${value.toFixed(decimals)}%`;

export const formatNumber = (value: number): string =>
  new Intl.NumberFormat('en-IN').format(value);

export const formatDate = (dateStr: string): string =>
  new Date(dateStr).toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric',
  });

export const getSegmentColor = (segment: string): string => {
  const colors: Record<string, string> = {
    'Platinum': '#E8D5B7',
    'Gold': '#FFD700',
    'Silver': '#C0C0C0',
    'New Investor': '#90EE90',
  };
  return colors[segment] || '#ccc';
};

export const getStatusColor = (status: string): 'success' | 'warning' | 'error' | 'default' => {
  const map: Record<string, any> = {
    Active: 'success',
    Matured: 'default',
    Cancelled: 'warning',
    Defaulted: 'error',
    Churned: 'error',
    Inactive: 'warning',
  };
  return map[status] || 'default';
};

export const CATEGORY_COLORS: Record<string, string> = {
  'Bond': '#4361EE',
  'Fixed Deposit': '#3A0CA3',
  'Invoice Discounting': '#7209B7',
  'Asset Leasing': '#F72585',
  'Digital Gold': '#FFB703',
  'Alternative Investment': '#06A77D',
};
