import React, {Component} from 'react'

import Overview from './subcomponents/main/Overview'
import TransferPage from './subcomponents/main/Transfer'
import './App.css';

const initialState = {
  route: 'overview',

}
class App extends Component { 

  constructor(props){
    super(props)
    this.state = initialState
  }

  onRouteChange = (dest) => {
    this.setState({route: dest})
  }
  render(){
    return (
      <div className="App">
        {this.state.route === 'overview' 
        ? 
          <Overview 
          onRouteChange={this.onRouteChange} /> 
        : 
          <TransferPage 
          onRouteChange={this.onRouteChange} />}
      </div>
    )
  }
} 

export default App;
