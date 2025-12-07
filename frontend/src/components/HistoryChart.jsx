import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';

export const HistoryChart = ({ data, testid }) => (
  <div className="h-[240px]" data-testid={testid}>
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={data}>
        <defs>
          <linearGradient id="c1" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#00CED1" stopOpacity="0.5" />
            <stop offset="100%" stopColor="#00CED1" stopOpacity="0" />
          </linearGradient>
        </defs>
        <XAxis dataKey="x" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip wrapperStyle={{ outline: 'none' }} />
        <Area type="monotone" dataKey="y" stroke="#00B3B5" fill="url(#c1)" strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  </div>
);
