/** @jsx React.DOM */

var size = 5;
var lastScrollTop = 0;
var min = 0;

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
		return {
			tweets: this.props.tweets,
			numPages: 0,
			count: 0,
			page: 0,
			paging: false,
			skip: 0,
			done: false
		};
	},

	loadPostsFromServer: function(self) {
		$.ajax({
			url: '/tweets',
			dataType: 'json',
			success: function(data){ 
				this.addTweet(data)
			}.bind(this),
			error: function(xhr, status, err) {
				console.error('/tweets', status, err.toString());
			}.bind(this)
		});
	},

	addTweet: function(tweets){
		var updated = this.state.tweets;
		var skip = this.state.skip + 1;
		var count = this.state.count;
		if(updated.length < tweets.length){
			tweets = tweets.slice(updated.length);
			tweets.forEach(function(tweet){
				count = count + 1;
				updated.push(tweet);
			});
			console.log(updated);
			this.setState({tweets: updated, count: count, skip: skip});
		}
	},

	checkWindowScroll: function(){

	    // Get scroll pos & window data
	    var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
	    var s = document.body.scrollTop;
	    var diff = lastScrollTop - s;
	    var totalMove = min - lastScrollTop;
	    var scrolled = (h + s) > document.body.offsetHeight - 100;

	    if(diff < 0 ){
	    	min = s;
	    }
	    // If scrolled enough, not currently paging and not complete...
	    if(scrolled && !this.state.paging && !this.state.done) {

	    	console.log('checking scroll triggered');
	      // Set application state (Paging, Increment page)
	      this.setState({paging: true, page: this.state.page + 1});

	      // Get the next page of tweets from the server
	      this.getPage();

	    } else if(totalMove > 400 && this.state.count > 20){
	    	console.log('remove ' + this.state.count);
	    	this.removeTweets(totalMove/168)
	    } else {
	    	console.log('nothing ' + s + ' ' + lastScrollTop);
	    	lastScrollTop = s;
	    }
	},

	removeTweets: function(number){
		console.log('scroll up triggerd for ' + number)
		var updated = this.state.tweets;
		var count = this.state.count;
		for(var i = 0; i < number; i++){
			updated.pop();
			count = count - 1;
		}

		this.setState({tweets: updated, count: count});

	},

	getPage: function(){

		var updated = this.state.tweets;
		var tweet = {"timestamp": "01/17/2015", "emoji": 4, "user_id": 1, "id": 28, "avatar": "http://www.gravatar.com/avatar/4b60a255f2ae71539a0111cb1ec5223a?d=mm&s=128", "location": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTgi5nDvtBwVJUZp4LoYou8lNUPF8CT1kO4XAstnCRYYHewRCwA"}
		updated.push(tweet);
		var count = this.state.count + 1;
		this.setState({tweets: updated});
		this.setState({paging: false, count: count, done: false});

	     //uncomment this later
	    //if (this.state.page < this.getNumPages()){

	        // Load our next page
			//self.loadNextPage();

	//	} else {

			// Set application state (Not paging, paging complete)
	//		self.setState({paging: false, done: true});

	//	}
    },

    loadNextPage: function(){

	    // So meta lol
	    var self = this;

	    // If we still have tweets...
	    if(this.state.page < this.getNumPages()) {

	      	// Get current application state
	      	var updated = this.state.tweets;
	      	var page = this.nextPage()

	      	page.data.forEach(function(tweet){
	      		update.push(tweet);
	      	});

	      	self.setState({tweets: updated, paging: false});
	    } else {

	    	// Set application state (Not paging, paging complete)
			self.setState({paging: false, done: true});

	    }
 	},

	nextPage: function(){
		var start = size* (this.state.page);
		var end = start + size;

		return {
			data: this.props.data.slice(start,end)
		}
	},

	componentDidMount: function() {
        this.loadPostsFromServer();
		window.addEventListener('scroll', this.checkWindowScroll);
	},

	render: function() {
		return (
			<div>
				<h1>Tweets</h1>
				<PostsList data={this.state.tweets}/>
			</div>
		);
	},

	getNumPages: function(){
		return Math.ceil(this.state.tweets.length /(height*width))
	},

	handlePageChange: function(pageNum) {
		this.setState({currentPage: pageNum})
	}
});
var init = [{"timestamp": "01/16/2015", "emoji": 4, "user_id": 2, "id": 28, "avatar": "http://www.gravatar.com/avatar/4b60a255f2ae71539a0111cb1ec5223a?d=mm&s=128", "location": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTgi5nDvtBwVJUZp4LoYou8lNUPF8CT1kO4XAstnCRYYHewRCwA"}]
React.renderComponent(
	<PostBox pollInterval={10000} tweets={init} />,
	document.getElementById('example')
);





