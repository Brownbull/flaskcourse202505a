import {Component} from 'react'
import {Table, Card, Button} from 'react-bootstrap'

import NavBar from './../navigation/Navigation'

class Overview extends Component {
    render() {
        return (
            <>
                <NavBar/>
                <Card>
                    <Card.Body>
                        <AccountInformation/>
                        <Button 
                        variant = 'primary'
                        onClick = {() => {this.props.onRouteChange('transfer')}}
                        >
                            Transfer
                        </Button>
                        <TransactionTable/>
                    </Card.Body>
                </Card>
            </>
        )
    }
}

class AccountInformation extends Component {
    render() {
        return (
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Account Number</th>
                        <th>Balance</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>My Name</td>
                        <td>Z009786608</td>
                        <td>100</td>
                    </tr>
                </tbody>
            </Table>
        )
    }
}

class TransactionTable extends Component {
    render() {
        return (
            <>  
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Transaction ID</th>
                            <th>From Acct</th>
                            <th>To Acct</th>
                            <th>Amount</th>
                            <th>Currency</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>Z009786608</td>
                            <td>Z009786608</td>
                            <th>50</th>
                            <th>Dollar</th>
                            <th>08-07-2025</th>
                        </tr>
                    </tbody>
                </Table>
            </>
            
        )
    }
}

export default Overview