import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, LineChart, Line, ResponsiveContainer } from 'recharts';
import { Droplet, Factory, Users, Warehouse } from 'lucide-react';

// Kenya AQUASTAT Data
const kenyaWaterData = {
  totalRenewableWaterResources: 30.7, // billion m³/year
  totalWaterWithdrawal: 3.218, // billion m³/year
  waterWithdrawalBySource: [
    { name: 'Surface Water', value: 2.165 },
    { name: 'Direct Use of Treated Wastewater', value: 0.032 },
  ],
  waterWithdrawalBySector: [
    { name: 'Agriculture', value: 2.165, percentage: 67.3 },
    { name: 'Industrial', value: 0.257, percentage: 8 },
    { name: 'Municipal', value: 0.795, percentage: 24.7 },
  ],
  waterStressData: [
    { year: '2000', value: 8.2 },
    { year: '2005', value: 9.1 },
    { year: '2010', value: 10.5 },
    { year: '2015', value: 11.2 },
    { year: '2020', value: 12.0 },
  ]
};

export default function KenyaWaterDashboard() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50 p-6">
      <h1 className="text-3xl font-bold mb-6">Kenya Water Resources Dashboard</h1>
      
      {/* Key Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Total Renewable Water</p>
                <p className="text-2xl font-bold">{kenyaWaterData.totalRenewableWaterResources} B m³/year</p>
              </div>
              <Droplet className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Total Withdrawal</p>
                <p className="text-2xl font-bold">{kenyaWaterData.totalWaterWithdrawal} B m³/year</p>
              </div>
              <Factory className="h-8 w-8 text-gray-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Agricultural Use</p>
                <p className="text-2xl font-bold">{kenyaWaterData.waterWithdrawalBySector[0].percentage}%</p>
              </div>
              <Warehouse className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Municipal Use</p>
                <p className="text-2xl font-bold">{kenyaWaterData.waterWithdrawalBySector[2].percentage}%</p>
              </div>
              <Users className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Water Withdrawal by Sector</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={kenyaWaterData.waterWithdrawalBySector}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="percentage" fill="#3b82f6" name="Percentage of Total Withdrawal" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Water Stress Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={kenyaWaterData.waterStressData}>
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="value" stroke="#3b82f6" name="Water Stress Level (%)" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Water Sources Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={kenyaWaterData.waterWithdrawalBySource}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#3b82f6" name="Billion m³/year" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}