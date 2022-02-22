import { MasterLayout } from "../core/MasterLayout"
import { TaxAccountantRoutes } from "./taxAccountantRoutes"

export const Routes: React.FC = (props) =>{

    var routes = <TaxAccountantRoutes/>
    return (
        <MasterLayout>
            {routes}
        </MasterLayout>
    )
}