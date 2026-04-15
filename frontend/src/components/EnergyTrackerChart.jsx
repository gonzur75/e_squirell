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
  BarElement
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import api from '../api';
import { Zap, Activity, BatteryCharging } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function EnergyTrackerChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data with hourly resolution
    api.get('/energy_tracker/?resolution=hourly')
      .then(response => {
        // Our endpoint returns an array or a paginated object if using pagination.
        // Assuming paginated `results` based on DRF standard
        const results = response.data.results || response.data;
        // Reverse array to show oldest to newest left to right
        setData([...results].reverse());
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="h-64 flex items-center justify-center text-slate-500 animate-pulse">Loading Energy Data...</div>;
  }

  // Format labels nicely
  const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));

  const powerData = {
    labels,
    datasets: [
      {
        label: 'Phase L1 Power',
        data: data.map(d => d.active_power_a),
        borderColor: '#ef4444', // Red
        backgroundColor: 'rgba(239, 68, 68, 0.5)',
        tension: 0.4
      },
      {
        label: 'Phase L2 Power',
        data: data.map(d => d.active_power_b),
        borderColor: '#eab308', // Yellow
        backgroundColor: 'rgba(234, 179, 8, 0.5)',
        tension: 0.4
      },
      {
        label: 'Phase L3 Power',
        data: data.map(d => d.active_power_c),
        borderColor: '#3b82f6', // Blue
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        tension: 0.4
      }
    ]
  };
  
  const currentData = {
    labels,
    datasets: [
      {
        label: 'L1 Current',
        data: data.map(d => d.current_a / 1000), // Assuming mA to A conversion if needed, adjust accordingly
        backgroundColor: '#ef4444',
      },
      {
        label: 'L2 Current',
        data: data.map(d => d.current_b / 1000),
        backgroundColor: '#eab308',
      },
      {
        label: 'L3 Current',
        data: data.map(d => d.current_c / 1000),
        backgroundColor: '#3b82f6',
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    hover: { mode: 'nearest', intersect: true },
    scales: {
      y: { beginAtZero: true }
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:shadow-md transition-shadow">
           <div className="h-12 w-12 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center"><Zap size={24}/></div>
           <div>
              <p className="text-sm text-slate-500 font-medium">Total Consumed (Last Entry)</p>
              <p className="text-2xl font-bold text-slate-800">
                {data.length > 0 ? (data[data.length-1].total_energy_consumed / 100).toFixed(2) : '--'}
              </p>
           </div>
        </div>
        <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:shadow-md transition-shadow">
           <div className="h-12 w-12 bg-red-50 text-red-500 rounded-full flex items-center justify-center"><Activity size={24}/></div>
           <div>
              <p className="text-sm text-slate-500 font-medium">Avg Active Power</p>
              <p className="text-2xl font-bold text-slate-800">
                 {data.length > 0 ? (data[data.length-1].total_active_power / 100).toFixed(0) : '--'} W
              </p>
           </div>
        </div>
        <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4 hover:shadow-md transition-shadow">
           <div className="h-12 w-12 bg-emerald-50 text-emerald-500 rounded-full flex items-center justify-center"><BatteryCharging size={24}/></div>
           <div>
              <p className="text-sm text-slate-500 font-medium">Grid Frequency</p>
              <p className="text-2xl font-bold text-slate-800">
                 {data.length > 0 ? (data[data.length-1].frequency / 100).toFixed(2) : '--'} Hz
              </p>
           </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl shadow-sn border border-slate-100 p-6">
          <h3 className="text-lg font-bold text-slate-800 mb-4 tracking-tight">Power Distribution (W)</h3>
          <div className="h-72">
            <Line options={options} data={powerData} />
          </div>
        </div>
        
        <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <h3 className="text-lg font-bold text-slate-800 mb-4 tracking-tight">Phase Current (A)</h3>
          <div className="h-72">
            <Bar options={options} data={currentData} />
          </div>
        </div>
      </div>
    </div>
  );
}
