import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import api from '../api';
import { Thermometer, Power, Flame, Calendar } from 'lucide-react';

export default function StorageHeaterChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [rawLatest, setRawLatest] = useState(null);

  useEffect(() => {
    // 1. Fetch aggregated history
    api.get('/storage_heater/?resolution=hourly')
      .then(response => {
        const results = response.data.results || response.data;
        setData([...results].reverse());
        setLoading(false);
      }).catch(err => {
        console.error(err);
        setLoading(false);
      });

    // 2. Fetch the true latest record from unaggregated endpoint just for Relays
    api.get('/storage_heater/')
      .then(response => {
        const rawResults = response.data.results || response.data;
        if (rawResults.length > 0) {
           setRawLatest(rawResults[0]);
        }
      }).catch(err => console.error("Latest fetch error", err));
  }, []);

  if (loading) {
    return <div className="h-64 flex flex-col items-center justify-center text-slate-400 animate-pulse">
        <Thermometer className="mb-4" size={40} />
        <p className="font-medium tracking-widest uppercase text-[10px]">Analyzing Thermal Retenion...</p>
    </div>;
  }

  const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Zone 1 (Living Room)',
        data: data.map(d => d.temp_one),
        borderColor: '#f97316',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 3
      },
      {
        label: 'Zone 2 (Bedroom)',
        data: data.map(d => d.temp_two),
        borderColor: '#8b5cf6',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 3
      },
      {
        label: 'Zone 3 (Bathroom)',
        data: data.map(d => d.temp_three),
        borderColor: '#06b6d4',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 3
      },
      {
        label: 'Zone 4 (Hallway)',
        data: data.map(d => d.temp_four),
        borderColor: '#10b981',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 3
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { 
        position: 'bottom',
        labels: { boxWidth: 8, usePointStyle: true, padding: 20, font: { size: 10, weight: 'bold' } }
      },
      tooltip: {
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        titleColor: '#1e293b',
        bodyColor: '#475569',
        borderColor: '#f1f5f9',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 12
      }
    },
    scales: {
      y: { grid: { color: 'rgba(0,0,0,0.02)' }, ticks: { font: { size: 10 } } },
      x: { grid: { display: false }, ticks: { font: { size: 10 } } }
    }
  };

  const Relays = ({ title, state }) => (
    <div className="flex items-center justify-between p-4 bg-slate-50 rounded-[1.25rem] border border-slate-100 hover:border-orange-200 transition-colors group">
       <span className="text-sm font-bold text-slate-700 tracking-tight">{title}</span>
       <div className={`h-4 w-4 rounded-full transition-all duration-500 scale-100 group-hover:scale-110 ${state ? 'bg-orange-500 shadow-[0_0_15px_rgba(249,115,22,0.6)]' : 'bg-slate-200'}`} />
    </div>
  );

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
      
      {/* Charts Section */}
      <div className="lg:col-span-3 bg-white p-8 rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-slate-100">
         <div className="flex items-center justify-between mb-8">
            <div className="flex items-center space-x-3">
               <div className="h-10 w-10 bg-orange-50 text-orange-500 rounded-2xl flex items-center justify-center">
                  <Thermometer size={20} />
               </div>
               <h3 className="text-xl font-black text-slate-800 tracking-tight">Thermal Retention</h3>
            </div>
            <div className="flex items-center space-x-2 text-[10px] font-black uppercase text-slate-400 tracking-widest px-3 py-1 bg-slate-50 rounded-full border border-slate-100">
               <Calendar size={12} className="mr-1" /> Last 24 Hours
            </div>
         </div>
         <div className="h-[400px]">
           <Line data={chartData} options={options} />
         </div>
      </div>

      {/* Relays Section */}
      <div className="bg-white p-8 rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-slate-100 flex flex-col h-full">
         <div className="flex items-center space-x-3 mb-8">
            <div className="h-10 w-10 bg-slate-900 text-white rounded-2xl flex items-center justify-center">
               <Flame size={20} />
            </div>
            <h3 className="text-xl font-black text-slate-800 tracking-tight">Active Heating</h3>
         </div>
         
         <div className="space-y-3 flex-grow">
             <Relays title="Living Room" state={rawLatest?.relay_one} />
             <Relays title="Master Bedroom" state={rawLatest?.relay_two} />
             <Relays title="Bathroom" state={rawLatest?.relay_three} />
             <Relays title="Main Hallway" state={rawLatest?.relay_four} />
             <Relays title="Aux Heater A" state={rawLatest?.relay_five} />
             <Relays title="Aux Heater B" state={rawLatest?.relay_six} />
         </div>

         <div className="mt-8 p-5 bg-blue-50 text-blue-800 text-[11px] font-bold rounded-2xl border border-blue-100 flex items-start space-x-3 leading-relaxed">
            <Power className="mt-0.5 shrink-0" size={16} />
            <p>Relays are currently managed by the hardware MCU. Remote overrides are read-only.</p>
         </div>
      </div>

    </div>
  );
}
