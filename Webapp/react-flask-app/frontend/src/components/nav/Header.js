import {Col, Container, Nav, Navbar, NavDropdown, Row} from "react-bootstrap"
import {ReactComponent as Logo} from "../../logo.svg"
import {useLocation} from "react-router-dom"

function Header() {
    let location = useLocation()

    console.log(location.pathname)
    return (
        <>
            <Row>
            <Col>
                <Navbar bg="light" expand="lg">
                    <Container fluid>
                        <Navbar.Brand href="/home">
                            <Logo width={"40px"} height={"40px"}/>
                            YouTube - Scraper</Navbar.Brand>
                        <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                        <Navbar.Collapse className="justify-content-end">
                            <Nav activeKey={location.pathname} className="container-fluid">
                                <NavDropdown title="Scraper" id="basic-nav-dropdown">
                                    <NavDropdown.Item href="/createvideojob">Video Scraper</NavDropdown.Item>
                                    <NavDropdown.Item href="/createcommentjob">Comment Scraper</NavDropdown.Item>
                                </NavDropdown>
                                <Nav.Link href="/translator">Translator</Nav.Link>
                                <NavDropdown title="API" id="basic-nav-dropdown">
                                    <NavDropdown.Item href="/createapi">Create API</NavDropdown.Item>
                                    <NavDropdown.Item href="/viewapis">View APIs</NavDropdown.Item>
                                </NavDropdown>
                                <Navbar.Text className="ms-auto">
                                    Signed in as: <a href="#login">Mark Otto</a>
                                </Navbar.Text>
                            </Nav>
                        </Navbar.Collapse>
                    </Container>
                </Navbar>
            </Col>
            </Row>
        </>
    )
}

export default Header

