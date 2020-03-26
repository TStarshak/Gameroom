import React, {Component} from 'react';
import MainMenu from './MainMenu/JS/MainMenu'
import './App.css';
import Notification from './MainMenu/JS/Notification';
import Rating from './Lobby/JS/Rating';
class App extends Component {
  constructor(props){
    super(props);
    this.user = {
      profileIcon: "https://i.ibb.co/sg0q559/Featherknight-Summoner-Icon-TFT-Lo-L.jpg",
      name: 'Scarria1',
      rating: 4.3
    }
    this.toNoti = this.toNoti.bind(this);
    this.toRating = this.toRating.bind(this);
    this.toMainMenu = this.toMainMenu.bind(this);
    this.state = {component: <MainMenu user={this.user} toNoti={this.toNoti}></MainMenu>};
  }

  toNoti(players){
    // console.log('to noti');
    this.setState({component: <Notification players={players} toRating={this.toRating}></Notification>});
    console.log(this.state);
  }

  toRating(players){
    this.setState({component: <Rating players={players} toMainMenu={this.toMainMenu}></Rating>});
  }

  toMainMenu(){
    this.setState({component: <MainMenu user={this.user} toNoti={this.toNoti}></MainMenu>});
  }
  render(){
    return (
      <div className="App">
        {this.state.component}
        {/* <Rating players= {[{name: 'Scarria1'},{name: 'Scarria2'},{name: 'Scarria3'},{name: 'Scarria4'},{name: 'Scarria5'}]}></Rating> */}
        {/* <Notification 
        players= {[{name: 'Scarria1'},{name: 'Scarria2'},{name: 'Scarria3'},{name: 'Scarria4'},{name: 'Scarria5'},{name: 'Scarria6'}]}
        ></Notification> */}
      </div>
    );
    
  }
} 
export default App;
