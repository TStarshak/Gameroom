import React, { Component } from 'react';
import io from 'socket.io-client';

import MainMenu from './MainMenu/JS/MainMenu'
import './App.css';
import Notification from './MainMenu/JS/Notification';
import Rating from './Lobby/JS/Rating';
import Lobby from './Lobby/JS/Lobby';
import Login from './Authenticate/JS/Login';
import Register from './Authenticate/JS/Register';



class App extends Component {
  constructor(props) {
    super(props);
    this.endpoint = 'localhost:5000';
    this.user = {
      profileIcon: "https://i.ibb.co/sg0q559/Featherknight-Summoner-Icon-TFT-Lo-L.jpg",
      name: 'Scarria1',
      rating: 4.3
    }
    this.toNoti = this.toNoti.bind(this);
    this.toRating = this.toRating.bind(this);
    this.toMainMenu = this.toMainMenu.bind(this);
    this.toRegister = this.toRegister.bind(this);
    this.toLogin = this.toLogin.bind(this);
    this.setUser = this.setUser.bind(this);
    this.register = this.register.bind(this);
    this.login = this.login.bind(this);
    this.matching = this.matching.bind(this);
    this.socket = null;
    this.state = {
      user: {},
      component: <Login toRegister={this.toRegister} login={this.login} incorrect={false}></Login>,
      room: {},
    }
    // this.state = {component: <MainMenu user={this.user} toNoti={this.toNoti}></MainMenu>};
  }
  // ___________________________________________________ API call____________________________

  setUser = (user) => {
    this.setState({ user: user });
  }

  register = (form_data) => {
    console.log(JSON.stringify(form_data))
    fetch('/api/player/create', {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form_data),
    })
      .then(res => res.json())
      .then((data) => {
        if (data.error == undefined) {
          this.login(form_data)
        }
        else {
          this.toRegister(true)
        }

      })
  }

  login = (form_data) => {
    fetch('/api/auth/login', {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form_data),
    })
      .then(res => res.json())
      .then((data) => {
        console.log(data)
        if (data.status == undefined) {
          this.setState({
            user: data,
          });
          this.socket = io(this.endpoint + '/connection');
          this.socket.on('connect_callback', data => console.log(data))
          this.toMainMenu();
        }
        else {
          this.toLogin(true)
        }
      })
  }

  matching = () => {
    fetch('/api/lobby/list', {
      method: 'GET', headers: {
        'Content-Type': 'application/json'
      },
    }).then(res => res.json())
    .then((data) => {
      console.log(data)
      let lobby_id = data[0].id;
      console.log(this.socket)
      this.socket.emit('match', {'lobby': lobby_id})
      this.socket.on('match', (data) => {
        this.setState({room: data.room})
        console.log(this.state.room)
        
      })
      this.toLobby()
    })
  }




  // __________________________________________________________ Transition_______________

  toLobby = () => {
    this.setState({component: <Lobby room={this.state.room} toRating={this.toRating}></Lobby>})
  }

  toRegister = (exist) => {
    this.setState({ component: <Register toLogin={this.toLogin} register={this.register} exist={exist}></Register> });
    console.log("to register")
  }

  toLogin = (incorrect) => {
    this.setState({ component: <Login toRegister={this.toRegister} login={this.login} incorrect={incorrect}></Login> })
    console.log("to login")
  }

  toNoti = (players) => {
    // console.log('to noti');
    this.setState({ component: <Notification players={players} toRating={this.toRating}></Notification> });
    console.log(this.state);
  }

  toRating = (players) => {
    this.setState({ component: <Rating players={players} toMainMenu={this.toMainMenu}></Rating> });
  }

  toMainMenu() {
    this.setState({ component: <MainMenu matching = {this.matching} all_players={this.state.all_players} user={this.state.user} toNoti={this.toNoti}></MainMenu> });
  }

  render() {
    return (
      <div className="App">
        {this.state.component}
        {/* <Login></Login> */}
        {/* <Lobby></Lobby> */}
        {/* {this.state.component} */}
        {/* <Rating players= {[{name: 'Scarria1'},{name: 'Scarria2'},{name: 'Scarria3'},{name: 'Scarria4'},{name: 'Scarria5'}]}></Rating> */}
        {/* <Notification 
        players= {[{name: 'Scarria1'},{name: 'Scarria2'},{name: 'Scarria3'},{name: 'Scarria4'},{name: 'Scarria5'},{name: 'Scarria6'}]}
        ></Notification> */}
      </div>
    );

  }
}
export default App;
