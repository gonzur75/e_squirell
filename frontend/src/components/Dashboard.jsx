import { useState, useEffect } from 'react';
import EnergyTrackerChart from './EnergyTrackerChart';
import StorageHeaterChart from './StorageHeaterChart';
import api from '../api';
import { Settings as SettingsIcon, Zap } from 'lucide-react';

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
    <div className="min-h-screen bg-slate-50 p-6 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-slate-200">
           <div>
              <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight flex items-center">
                 <Zap className="mr-2 text-blue-500" /> E-Squirell Dashboard
              </h1>
              <p className="text-slate-500 mt-1">Smart Energy & Heating Monitor</p>
           </div>
           
           {/* Global Settings Quick Control */}
           {settings && (
               <div className="mt-4 md:mt-0 flex items-center space-x-3 bg-white px-4 py-2 rounded-xl shadow-sm border border-slate-200">
                  <SettingsIcon className="text-slate-400" size={20} />
                  <span className="text-sm font-semibold text-slate-700">Master Heating:</span>
                  <button 
                     onClick={handleHeatingToggle}
                     className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ${settings.heating_required ? 'bg-orange-500' : 'bg-slate-300'}`}
                  >
                     <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${settings.heating_required ? 'translate-x-6' : 'translate-x-1'}`} />
                  </button>
               </div>
           )}
        </header>

        {/* Phase Monitors */}
        <section>
           <h2 className="text-xl font-bold text-slate-800 mb-4 tracking-tight">Real-time Energy Analytics</h2>
           <EnergyTrackerChart />
        </section>

        {/* Heater Monitors */}
        <section className="pt-6">
           <h2 className="text-xl font-bold text-slate-800 mb-4 tracking-tight">Thermal Storage Heaters</h2>
           <StorageHeaterChart />
        </section>

      </div>
    </div>
  );
}
