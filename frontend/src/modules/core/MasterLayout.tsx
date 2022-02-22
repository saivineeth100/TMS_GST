import { Container } from "react-bootstrap"


const MasterLayout: React.FC = ({ children }) => {

    return (
            <Container fluid>
                <header className="bg-light sticky-top">
                    {/* <NavigationMenu /> */}
                </header>

                {children}
               

            </Container>)
}
export { MasterLayout }