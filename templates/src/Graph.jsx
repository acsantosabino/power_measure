var React = require('react');

var Graph = React.createClass({
  getInitialState: function() {
    return { imageStatus: null };
  },
  handleImageLoaded() {
    this.setState({ imageStatus: 'loaded' });
  },
  handleImageErrored() {
    this.setState({ imageStatus: 'failed to load' });
  },
  componentDidMount: function() {
    this.render();
    setInterval(this.render, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="box graph">
        <img src={this.props.url}/>
      </div>
    );
  }
});

module.exports = Graph;
