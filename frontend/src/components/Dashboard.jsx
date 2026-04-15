import { useState, useEffect } from 'react';
import EnergyTrackerChart from './EnergyTrackerChart';
import StorageHeaterChart from './StorageHeaterChart';
import api from '../api';
import { Settings as SettingsIcon, Zap, Shield, Cpu } from 'lucide-react';

export default function Dashboard() {
  const [settings, setSettings] = useState(null);

  useEffect(() => {
    // Fetch global configuration
    api.get('/core/settings/1/')
      .then(res => setSettings(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleHeatingToggle = () => {
    if (!settings) return;
    const newStatus = !settings.heating_required;
    api.patch('/core/settings/1/', { heating_required: newStatus })
      .then(res => setSettings(res.data))
      .catch(err => console.error(err));
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] p-4 md:p-8 font-sans selection:bg-blue-100">
      <div className="max-w-7xl mx-auto space-y-12">
        
        {/* Premium Header */}
        <header className="relative overflow-hidden bg-slate-900 rounded-[3rem] p-8 md:p-12 shadow-2xl shadow-slate-900/20">
           {/* Decorative Background Elements */}
           <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-blue-500/10 rounded-full blur-[100px]"></div>
           <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-72 h-72 bg-emerald-500/10 rounded-full blur-[80px]"></div>

           <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-8">
              <div className="flex items-center space-x-6">
                 <div className="h-16 w-16 bg-blue-500 rounded-3xl flex items-center justify-center shadow-lg shadow-blue-500/40 rotate-12 group hover:rotate-0 transition-transform duration-500">
                    <Zap className="text-white" size={32} fill="currentColor" />
                 </div>
                 <div>
                    <h1 className="text-4xl font-black text-white tracking-tight flex items-center">
                       E-Squirell <span className="ml-3 text-sm font-bold bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full border border-blue-500/30 uppercase tracking-widest">v2.0</span>
                    </h1>
                    <p className="text-slate-400 mt-2 font-medium flex items-center">
                       <Shield size={14} className="mr-2 text-emerald-500" /> Secure Grid Monitoring & Thermal Optimization
                    </p>
                 </div>
              </div>
              
              {/* Controls */}
              <div className="flex flex-wrap items-center gap-4">
                 <div className="flex items-center space-x-2 bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 px-3 py-1.5 rounded-2xl">
                    <Cpu size={14} className="text-slate-500" />
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter text-nowrap">Hardware Node: Active</span>
                    <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
                 </div>

                 {settings && (
                    <div className="flex items-center space-x-4 bg-white/5 backdrop-blur-md px-6 py-3 rounded-[2rem] border border-white/10 shadow-inner">
                       <span className="text-sm font-bold text-slate-300">Auto Harvest Mode</span>
                       <button 
                          onClick={handleHeatingToggle}
                          className={`relative inline-flex h-7 w-14 items-center rounded-full transition-all duration-500 focus:outline-none ${settings.heating_required ? 'bg-orange-500 shadow-lg shadow-orange-500/50' : 'bg-slate-700'}`}
                       >
                          <span className={`inline-block h-5 w-5 transform rounded-full bg-white shadow-md transition-all duration-500 ${settings.heating_required ? 'translate-x-8' : 'translate-x-1'}`} />
                       </button>
                    </div>
                 )}
              </div>
           </div>
        </header>

        {/* Analytics Grid */}
        <div className="grid grid-cols-1 gap-12">
           {/* Phase Monitors */}
           <section>
              <div className="flex items-center justify-between mb-8 px-4">
                 <h2 className="text-2xl font-black text-slate-900 tracking-tight">Real-time Energy Analytics</h2>
                 <div className="h-px flex-grow mx-8 bg-slate-200 hidden md:block"></div>
                 <div className="text-xs font-bold text-slate-400 uppercase tracking-widest">Grid Metrics</div>
              </div>
              <EnergyTrackerChart />
           </section>

           {/* Heater Monitors */}
           <section>
              <div className="flex items-center justify-between mb-8 px-4">
                 <h2 className="text-2xl font-black text-slate-900 tracking-tight">Thermal Storage Heaters</h2>
                 <div className="h-px flex-grow mx-8 bg-slate-200 hidden md:block"></div>
                 <div className="text-xs font-bold text-slate-400 uppercase tracking-widest">Climate Control</div>
              </div>
              <StorageHeaterChart />
           </section>
        </div>

      </div>
    </div>
  );
}
