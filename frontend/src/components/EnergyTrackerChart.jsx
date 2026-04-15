import { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
  Filler
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import api from '../api';
import { Zap, Activity, BatteryCharging, ArrowDownLeft, ArrowUpRight } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export default function EnergyTrackerChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/energy_tracker/?resolution=hourly')
      .then(response => {
        const results = response.data.results || response.data;
        setData([...results].reverse());
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="h-96 flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-400 font-medium animate-pulse">Synchronizing Grid Data...</p>
      </div>
    );
  }

  const latest = data.length > 0 ? data[data.length - 1] : null;
  const netPower = latest ? (latest.total_active_power) : 0;
  const consumption = netPower > 0 ? netPower : 0;
  const production = netPower < 0 ? Math.abs(netPower) : 0;

  const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));

  const powerData = {
    labels,
    datasets: [
      {
        label: 'Net Power (W)',
        data: data.map(d => d.total_active_power),
        borderColor: (context) => {
           const chart = context.chart;
           const {ctx, chartArea} = chart;
           if (!chartArea) return null;
           const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
           gradient.addColorStop(0, '#f43f5e'); // Rose (Import)
           gradient.addColorStop(0.5, '#cbd5e1'); // Neutral
           gradient.addColorStop(1, '#10b981'); // Emerald (Export)
           return gradient;
        },
        backgroundColor: 'rgba(59, 130, 246, 0.05)',
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 6,
        borderWidth: 3
      }
    ]
  };

  const phaseData = {
    labels,
    datasets: [
      {
        label: 'L1',
        data: data.map(d => d.active_power_a),
        borderColor: '#f43f5e',
        backgroundColor: 'transparent',
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0
      },
      {
        label: 'L2',
        data: data.map(d => d.active_power_b),
        borderColor: '#fbbf24',
        backgroundColor: 'transparent',
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0
      },
      {
        label: 'L3',
        data: data.map(d => d.active_power_c),
        borderColor: '#3b82f6',
        backgroundColor: 'transparent',
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        titleColor: '#1e293b',
        bodyColor: '#475569',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 12,
        usePointStyle: true
      },
    },
    scales: {
      y: {
        grid: { color: 'rgba(0,0,0,0.03)' },
        ticks: { color: '#94a3b8', font: { size: 11 } }
      },
      x: {
        grid: { display: false },
        ticks: { color: '#94a3b8', font: { size: 11 }, maxRotation: 0 }
      }
    }
  };

  return (
    <div className="space-y-8">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        {/* Consumption Card */}
        <div className="relative overflow-hidden bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100 group hover:shadow-xl transition-all duration-500">
           <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <ArrowDownLeft size={80} className="text-rose-500" />
           </div>
           <div className="relative z-10 flex flex-col h-full justify-between">
              <div className="flex items-center space-x-3 mb-4">
                 <div className="h-10 w-10 bg-rose-50 text-rose-500 rounded-2xl flex items-center justify-center">
                    <Zap size={20} fill="currentColor" />
                 </div>
                 <span className="text-sm font-bold text-rose-600/70 uppercase tracking-widest">Consumption</span>
              </div>
              <div>
                 <p className="text-4xl font-black text-slate-800 tracking-tighter">
                    {consumption.toLocaleString()} <span className="text-lg font-medium text-slate-400">W</span>
                 </p>
                 <p className="text-xs text-slate-400 mt-2 font-medium">Current Power Import</p>
              </div>
           </div>
        </div>

        {/* Production Card */}
        <div className="relative overflow-hidden bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100 group hover:shadow-xl transition-all duration-500">
           <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <ArrowUpRight size={80} className="text-emerald-500" />
           </div>
           <div className="relative z-10 flex flex-col h-full justify-between">
              <div className="flex items-center space-x-3 mb-4">
                 <div className="h-10 w-10 bg-emerald-50 text-emerald-500 rounded-2xl flex items-center justify-center">
                    <BatteryCharging size={20} fill="currentColor" />
                 </div>
                 <span className="text-sm font-bold text-emerald-600/70 uppercase tracking-widest">Production</span>
              </div>
              <div>
                 <p className="text-4xl font-black text-slate-800 tracking-tighter">
                    {production.toLocaleString()} <span className="text-lg font-medium text-slate-400">W</span>
                 </p>
                 <p className="text-xs text-slate-400 mt-2 font-medium">Current Power Export</p>
              </div>
           </div>
        </div>

        {/* Frequency Card */}
        <div className="bg-slate-900 p-6 rounded-[2rem] shadow-xl border border-slate-800 flex flex-col justify-between">
           <div className="flex items-center space-x-3 mb-4">
              <div className="h-10 w-10 bg-blue-500/10 text-blue-400 rounded-2xl flex items-center justify-center">
                 <Activity size={20} />
              </div>
              <span className="text-sm font-bold text-blue-400 uppercase tracking-widest">Grid Frequency</span>
           </div>
           <div>
              <p className="text-4xl font-black text-white tracking-tighter">
                 {latest ? (latest.frequency / 100).toFixed(2) : '--'} <span className="text-lg font-medium text-slate-500">Hz</span>
              </p>
              <div className="flex items-center mt-2 space-x-2">
                 <div className="h-1.5 w-12 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-blue-500 w-3/4 animate-pulse"></div>
                 </div>
                 <span className="text-[10px] text-slate-500 font-bold uppercase">Stable Range</span>
              </div>
           </div>
        </div>

        {/* Status Card */}
        <div className={`p-6 rounded-[2rem] border transition-colors duration-500 flex flex-col justify-between ${netPower <= 0 ? 'bg-emerald-500 border-emerald-400 shadow-emerald-200 shadow-lg' : 'bg-white border-slate-100 shadow-sm'}`}>
           <span className={`text-[10px] font-black uppercase tracking-[0.2em] ${netPower <= 0 ? 'text-emerald-100' : 'text-slate-400'}`}>System Status</span>
           <div className="mt-4">
              <p className={`text-2xl font-black leading-tight ${netPower <= 0 ? 'text-white' : 'text-slate-800'}`}>
                 {netPower <= 0 ? 'Energy Surplus' : 'Drawing from Grid'}
              </p>
              <p className={`text-xs mt-1 font-medium ${netPower <= 0 ? 'text-emerald-100' : 'text-slate-400'}`}>
                 {netPower <= 0 ? 'Optimizing local storage...' : 'Normal grid operations'}
              </p>
           </div>
        </div>

      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Main Power Chart */}
        <div className="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-slate-100 p-8">
           <div className="flex items-center justify-between mb-8">
              <div>
                 <h3 className="text-xl font-black text-slate-800 tracking-tight">Net Power Flow</h3>
                 <p className="text-xs text-slate-400 font-medium">Bi-directional monitoring (W)</p>
              </div>
              <div className="flex items-center space-x-2 bg-slate-50 p-1 rounded-xl border border-slate-100 text-[10px] font-bold text-slate-500 uppercase tracking-tighter">
                 <span className="px-2 py-1 rounded-lg bg-white shadow-sm border border-slate-200">24h History</span>
                 <span className="px-2">Live</span>
              </div>
           </div>
           <div className="h-80">
              <Line options={options} data={powerData} />
           </div>
        </div>

        {/* Phase Analysis */}
        <div className="bg-white rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-slate-100 p-8">
           <div className="flex items-center justify-between mb-8">
              <div>
                 <h3 className="text-xl font-black text-slate-800 tracking-tight">Phase Performance</h3>
                 <p className="text-xs text-slate-400 font-medium">Real-time load split (W)</p>
              </div>
              <div className="flex space-x-2">
                 <div className="h-2 w-2 rounded-full bg-rose-500"></div>
                 <div className="h-2 w-2 rounded-full bg-amber-400"></div>
                 <div className="h-2 w-2 rounded-full bg-blue-500"></div>
              </div>
           </div>
           <div className="h-80">
              <Line options={options} data={phaseData} />
           </div>
        </div>

      </div>
    </div>
  );
}
