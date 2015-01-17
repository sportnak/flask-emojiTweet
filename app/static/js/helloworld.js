/** @jsx React.DOM */

var size = 5;

var Post = React.createClass({
	render: function() {
		return (
			<div class="container">	
				<div class="row">
					<div class="span8 offset2" style={{textAlign:'center'}}>
						<h2><img src={ this.props.post.avatar }></img><i> {this.props.post.nickname } is feeling: </i><img src={ this.props.post.location } height="100" width="100"></img></h2><p>on { this.props.post.timestamp }</p>
					</div>
				</div>
			</div>
		);
	}
});

var PostsList = React.createClass({
	render: function() {
		//var page = this.getPage()
		var postNodes = this.props.data.map(function(post){
			return (
				<Post post={post} />
			);
		});
		return (
			<div className="postList">
				{postNodes}
			</div>
		);
	},

	getPage: function(){
		var start = size* (this.state.currentPage - 1);
		var end = start + size;

		return {
			currentPage: this.state.currentPage,
			data: this.props.data.slice(start,end),
			numPages: this.getNumPages(),
			handleClick: function(pageNum) {
				return function() {
					this.handlePageChange(pageNum)
				}.bind(this)
			}.bind(this)
		}
	},

	getNumPages: function(){
		return Math.ceil(this.props.data.length /(height*width))
	},

	handlePageChange: function(pageNum) {
		this.setState({currentPage: pageNum})
	}
});

var SetIntervalMixin = {
  componentWillMount: function() {
    this.intervals = [];
  },
  setInterval: function() {
    this.intervals.push(setInterval.apply(null, arguments));
  },
  componentWillUnmount: function() {
    this.intervals.map(clearInterval);
  }
};

var PostBox = React.createClass({
	mixins: [SetIntervalMixin], // Use the mixin
	getInitialState: function() {
		return {data: []}
	},
	loadPostsFromServer: function() {
		$.ajax({
			url: '/tweets',
			dataType: 'json',
			success: function(data){
				this.setState({data: data});
			}.bind(this),
			error: function(xhr, status, err) {
				console.error('/tweets', status, err.toString());
			}.bind(this)
		});
	},
	componentWillMount: function() {
        this.loadPostsFromServer();
        this.setInterval(this.loadPostsFromServer, this.props.pollInterval);
    },
	render: function() {
		return (
			<div>
				<h1>Tweets</h1>
				<PostsList data={this.state.data}/>
			</div>
			);
	}
});

React.renderComponent(
	<PostBox pollInterval={10000}/>,
	document.getElementById('example')
);

