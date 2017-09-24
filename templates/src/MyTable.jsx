var React = require("react");

var TableList = React.createClass({
  sortKeys: function(a) {
        var keys = [];
        for (var key in a) {
           keys.push(key);
        }
        keys.sort();
    return keys;
  },
  render: function() {
    var self = this;
    var tableFirstLine = this.props.data.map(function(measure, i) {
      var tableColums = [];
      if (i==0) {
        var keys = self.sortKeys(measure);
        for (var index in keys){
          tableColums.push(<th  className="table cell">{keys[index].replace("_"," ")}</th>);
        }}
      return (<tr className="table cell">{tableColums}</tr>);
    });
    var tableLines = this.props.data.map(function(measure, i) {
      var tableColums = [];
      var keys = self.sortKeys(measure);
      for (var index in keys){
        tableColums.push(<td className="table cell">{measure[keys[index]]}</td>);
      }
      return (<tr className="table cell">{tableColums}</tr>);
    });
    return (
      <table className="table history">
        {tableFirstLine}
        {tableLines}
      </table>
    );
  }
});

var MyTable = React.createClass({
  loadCommentsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.loadCommentsFromServer();
    setInterval(this.loadCommentsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="box history" >
        <table className="table history">
          <tr><th>{this.props.title}</th></tr>
        </table>
         <TableList data={this.state.data} />
      </div>
    );
  }
});

module.exports = MyTable;
