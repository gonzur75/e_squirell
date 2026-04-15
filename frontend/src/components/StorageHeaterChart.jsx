import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import api from '../api';
import { Thermometer, Power, Flame } from 'lucide-react';

export default function StorageHeaterChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  // In read-only mode, we still try to get the latest raw data 
  // to fetch the real current relay state, but since the requirement 
  // was ?resolution=hourly, relays might be missing or averaged out.
  // We handle gracefully.
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
    return <div className="h-64 flex items-center justify-center text-slate-500 animate-pulse">Loading Storage Heater...</div>;
  }

  const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Zone 1 (Living Room)',
        data: data.map(d => d.temp_one),
        borderColor: '#f97316', // Orange
        tension: 0.3
      },
      {
        label: 'Zone 2 (Bedroom)',
        data: data.map(d => d.temp_two),
        borderColor: '#8b5cf6', // Violet
        tension: 0.3
      },
      {
        label: 'Zone 3 (Bathroom)',
        data: data.map(d => d.temp_three),
        borderColor: '#06b6d4', // Cyan
        tension: 0.3
      },
      {
        label: 'Zone 4 (Hallway)',
        data: data.map(d => d.temp_four),
        borderColor: '#10b981', // Emerald
        tension: 0.3
      }
    ]
  };

  const Relays = ({ title, state }) => (
    <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
       <span className="text-sm font-medium text-slate-700">{title}</span>
       <div className={`h-3 w-3 rounded-full ${state ? 'bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.8)]' : 'bg-slate-300'}`} />
    </div>
  );

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      
      {/* Charts Section */}
      <div className="lg:col-span-3 bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
         <div className="flex items-center space-x-2 mb-4">
            <Thermometer className="text-orange-500" />
            <h3 className="text-lg font-bold text-slate-800 tracking-tight">Thermal Retention</h3>
         </div>
         <div className="h-[350px]">
           <Line 
             data={chartData} 
             options={{
               responsive: true,
               maintainAspectRatio: false,
               plugins: { legend: { position: 'bottom' } },
               scales: { y: { beginAtZero: false } }
             }} 
           />
         </div>
      </div>

      {/* Relays Section (Read Only) */}
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
         <div className="flex items-center space-x-2 mb-6">
            <Flame className="text-orange-500" />
            <h3 className="text-lg font-bold text-slate-800 tracking-tight">Active Heating</h3>
         </div>
         
         <div className="space-y-3">
             <Relays title="Zone 1 Element" state={rawLatest?.relay_one} />
             <Relays title="Zone 2 Element" state={rawLatest?.relay_two} />
             <Relays title="Zone 3 Element" state={rawLatest?.relay_three} />
             <Relays title="Zone 4 Element" state={rawLatest?.relay_four} />
             <Relays title="Aux Heater A" state={rawLatest?.relay_five} />
             <Relays title="Aux Heater B" state={rawLatest?.relay_six} />
         </div>

         <div className="mt-8 p-4 bg-orange-50 text-orange-800 text-sm rounded-xl border border-orange-100 flex items-start space-x-3">
            <Power className="mt-0.5" size={18} />
            <p>Relays are currently in automated hardware mode. Remote overrides disabled.</p>
         </div>
      </div>

    </div>
  );
}
