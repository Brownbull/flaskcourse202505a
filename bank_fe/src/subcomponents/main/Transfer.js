import { Component } from 'react'
import { Form, Card, Button } from 'react-bootstrap'

import NavBar from './../navigation/Navigation'

class TransferPage extends Component {
    render() {
        return (
            <>
                <NavBar/>
                <Card>
                    <Card.Body>
                        <TransferForm/>
                        <Button variant='primary'>Transfer</Button>
                    </Card.Body>
                </Card>
            </>
        )
    }
}

class TransferForm extends Component {
    render() {
        return (
            <>
                <Form>
                    <Form.Group class="mb-3">
                        <Form.Label>From</Form.Label>
                        <Form.Control type='text' />
                    </Form.Group>
                    <Form.Group class="mb-3">
                        <Form.Label>To</Form.Label>
                        <Form.Control type='text' />
                    </Form.Group>
                    <Form.Group class="mb-3">
                        <Form.Label>Amount</Form.Label>
                        <Form.Control type='text' />
                    </Form.Group>
                </Form>
            </>
        )
    }
}

export default TransferPage