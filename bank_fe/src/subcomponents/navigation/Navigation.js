import { Component } from 'react'
import { Navbar, Button } from 'react-bootstrap'

import './Navigation.css'

class NavBar extends Component {
    render() {
        return (
            <>
                <Navbar bg="light" expand="lg" fixed='top'>
                    <Button>Overview</Button>
                </Navbar>
            </>
        )
    }
}

export default NavBar