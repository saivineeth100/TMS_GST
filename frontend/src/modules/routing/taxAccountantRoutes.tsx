import { Routes, Route } from "react-router-dom";
import { TaxAccountantDashboard } from "../TaxAccountant/dashboard";

export function TaxAccountantRoutes() {
    
    return (
        <Routes>
            <Route path="/dashboard" element={<TaxAccountantDashboard/>} />
        </Routes>)
}  