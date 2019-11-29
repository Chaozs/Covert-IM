class Post {
  final String body;

  Post({this.body});

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      body: json['body'],
    );
  }
}