import {Tab, Tabs} from "react-bootstrap";

function TabView() {
    return (
        <div className="h-100 d-inline-block">
            <Tabs defaultActiveKey="profile" id="uncontrolled-tab-example" className="mb-3">
                <Tab eventKey="home" title="Home">
                    <p>home</p>
                </Tab>
                <Tab eventKey="profile" title="Profile">
                    <p>profile</p>
                </Tab>
                <Tab eventKey="contact" title="Contact" disabled>
                    <p>contact</p>
                </Tab>
            </Tabs>

        </div>
    )

}

export default TabView
