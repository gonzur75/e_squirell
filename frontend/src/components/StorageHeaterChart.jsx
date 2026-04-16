import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import api from '../api';
import { Thermometer, Power, Flame, Calendar } from 'lucide-react';

export default function StorageHeaterChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [resolution, setResolution] = useState('hourly');
  const [rawLatest, setRawLatest] = useState(null);

  useEffect(() => {
    // 1. Fetch aggregated history
    setLoading(true);
    api.get(`/storage_heater/?resolution=${resolution}`)
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

  const labels = data.map(d => {
    const date = new Date(d.timestamp);
    if (resolution === 'hourly') {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (resolution === 'daily') {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    } else {
      return date.toLocaleDateString([], { month: 'short', year: 'numeric' });
    }
  });

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Tank Top (100%)',
        data: data.map(d => d.temp_one),
        borderColor: '#f97316',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 3
      },
      {
        label: 'Tank 75%',
        data: data.map(d => d.temp_two),
        borderColor: '#8b5cf6',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 3
      },
      {
        label: 'Tank 50%',
        data: data.map(d => d.temp_three),
        borderColor: '#06b6d4',
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 3
      },
      {
        label: 'Tank Bottom (25%)',
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

  const HeaterKnob = ({ active, kw, positionClasses }) => (
    <div className={`absolute ${positionClasses} flex items-center justify-center w-8 h-8 rounded-full border-2 transition-all duration-500 z-20 ${active ? 'bg-orange-500 border-orange-300 shadow-[0_0_20px_rgba(249,115,22,1)] scale-110' : 'bg-slate-200 border-slate-300 shadow-inner'}`}>
      <span className={`text-[9px] font-black ${active ? 'text-white' : 'text-slate-500'}`}>{kw}</span>
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
            <div className="flex items-center space-x-1 bg-slate-50 p-1 rounded-xl border border-slate-100 text-[10px] font-bold text-slate-500 uppercase tracking-tighter">
               <button onClick={() => setResolution('hourly')} className={`px-3 py-1.5 rounded-lg transition-all ${resolution === 'hourly' ? 'bg-white shadow-sm border border-slate-200 text-slate-800' : 'hover:bg-slate-200/50'}`}>24h</button>
               <button onClick={() => setResolution('daily')} className={`px-3 py-1.5 rounded-lg transition-all ${resolution === 'daily' ? 'bg-white shadow-sm border border-slate-200 text-slate-800' : 'hover:bg-slate-200/50'}`}>Month</button>
               <button onClick={() => setResolution('monthly')} className={`px-3 py-1.5 rounded-lg transition-all ${resolution === 'monthly' ? 'bg-white shadow-sm border border-slate-200 text-slate-800' : 'hover:bg-slate-200/50'}`}>Year</button>
            </div>
         </div>
         <div className="h-[400px]">
           <Line data={chartData} options={options} />
         </div>
      </div>

      {/* Relays Section */}
      <div className="bg-white p-8 rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-slate-100 flex flex-col h-full">
         <div className="flex items-center justify-between mb-8">
            <div className="flex items-center space-x-3">
               <div className="h-10 w-10 bg-slate-900 text-white rounded-2xl flex items-center justify-center">
                  <Flame size={20} />
               </div>
               <h3 className="text-lg font-black text-slate-800 tracking-tight">2300L Buffer Tank</h3>
            </div>
         </div>
         
         <div className="flex-grow flex items-center justify-center relative py-4">
            {/* The Tank Graphic */}
            <div className="w-32 h-64 bg-slate-100 rounded-[2rem] border-[6px] border-slate-300 relative shadow-inner overflow-hidden flex flex-col justify-between">
               {/* Water gradient approximation (hot top, cool bottom default, overlaid with uniform style) */}
               <div className="absolute inset-x-0 bottom-0 top-[10%] bg-gradient-to-b from-rose-400 via-orange-300 to-cyan-300 opacity-30"></div>
               
               {/* 100% sensor */}
               <div className="flex-1 w-full flex items-center justify-between px-2 z-10 border-b border-white/30">
                  <div className="text-[9px] font-black text-slate-500 bg-white/80 px-1 rounded shadow-sm">100%</div>
                  <div className="text-xs font-black text-slate-800 drop-shadow-md">{rawLatest?.temp_one?.toFixed(1) || '--'}°</div>
               </div>
               {/* 75% sensor */}
               <div className="flex-1 w-full flex items-center justify-between px-2 z-10 border-b border-white/30">
                  <div className="text-[9px] font-black text-slate-500 bg-white/80 px-1 rounded shadow-sm">75%</div>
                  <div className="text-xs font-black text-slate-800 drop-shadow-md">{rawLatest?.temp_two?.toFixed(1) || '--'}°</div>
               </div>
               {/* 50% sensor */}
               <div className="flex-1 w-full flex items-center justify-between px-2 z-10 border-b border-white/30">
                  <div className="text-[9px] font-black text-slate-500 bg-white/80 px-1 rounded shadow-sm">50%</div>
                  <div className="text-xs font-black text-slate-800 drop-shadow-md">{rawLatest?.temp_three?.toFixed(1) || '--'}°</div>
               </div>
               {/* 25% sensor */}
               <div className="flex-1 w-full flex items-center justify-between px-2 z-10">
                  <div className="text-[9px] font-black text-slate-500 bg-white/80 px-1 rounded shadow-sm">25%</div>
                  <div className="text-xs font-black text-slate-800 drop-shadow-md">{rawLatest?.temp_four?.toFixed(1) || '--'}°</div>
               </div>
            </div>

            {/* Heaters mounted on the sides of the tank container */}
            <HeaterKnob active={rawLatest?.relay_one} kw="1kW" positionClasses="-left-2 top-[15%]" />
            <HeaterKnob active={rawLatest?.relay_two} kw="1kW" positionClasses="-left-2 top-[40%]" />
            <HeaterKnob active={rawLatest?.relay_three} kw="1kW" positionClasses="-left-2 top-[65%]" />

            <HeaterKnob active={rawLatest?.relay_four} kw="2kW" positionClasses="-right-2 top-[30%]" />
            <HeaterKnob active={rawLatest?.relay_five} kw="2kW" positionClasses="-right-2 top-[55%]" />
            <HeaterKnob active={rawLatest?.relay_six} kw="2kW" positionClasses="-right-2 top-[80%]" />
         </div>

         <div className="mt-8 p-4 bg-orange-50 text-orange-800 text-[10px] font-bold rounded-2xl border border-orange-100 flex items-start space-x-3 leading-tight">
            <Power className="mt-0.5 shrink-0 text-orange-500" size={14} />
            <p>Safety Limit: 85°C. Heating elements activate automatically when surplus solar power is detected.</p>
         </div>
      </div>

    </div>
  );
}
