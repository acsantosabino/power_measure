var $ = require('jquery');
var React = require('react');

var Device = React.createClass({
  loadCommentsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({dev_name: data.dev_name});
        this.setState({power: data.power});
        this.setState({consume_class: data.consume_class});
      }.bind(this),
      error: function(xhr, status, err) {
        this.getInitialState()
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {dev_name: '', power: '',consume_class: 'A'};
  },
  handleDevNameChange: function(e) {
    this.setState({dev_name: e.target.value});
  },
  handlePowerChange: function(e) {
    this.setState({power: e.target.value});
  },
  handleConsumeClassChange: function(e) {
    this.setState({consume_class: e.target.value});
  },
  handleSubmit: function(devinfo) {
    devinfo.preventDefault();
    var dev_name = this.state.dev_name.trim();
    var power = this.state.power.trim();
    var consume_class = this.state.consume_class.trim();
    if (!dev_name || !power) {
      console.error(this.props.url, status,'empty data');
      return;
    }
    var data = {dev_name: dev_name, power: power,consume_class: consume_class};
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data: data,
      success: function(data) {
        this.setState({dev_name: data.dev_name});
        this.setState({power: data.power});
        this.setState({consume_class: data.consume_class});
      }.bind(this),
      error: function(xhr, status, err) {
        this.getInitialState()
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function() {
    this.loadCommentsFromServer();
  },
  render: function() {
    return (
      <div className="box config" onLoad={this.loadCommentsFromServer}>
        <form className="devInfo" onSubmit={this.handleSubmit}>
          <div>
          <label>Device Name</label>
          <input
            type="text"
            placeholder="Device Name"
            value={this.state.dev_name}
            onChange={this.handleDevNameChange}
            className="input name"
          />
          </div>
          <div>
          <label className='firstLabel'>Device Power</label>
          <label>Class</label>
          <input
            type="number"
            placeholder="0"
            value={this.state.power}
            onChange={this.handlePowerChange}
            className="input power"
          />
          <select
            value={this.state.consume_class}
            onChange={this.handleConsumeClassChange}>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
            <option value="E">E</option>
            <option value="F">F</option>
            <option value="G">G</option>
          </select>
          </div>
          <input type="submit" value="Post" />
        </form>
      </div>
    );
  }
});

module.exports = Device;
