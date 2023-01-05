 -> POST   
 {
    user: {
        username: quad,
        profile_pic: 'profile/',
        profile_link: "http:localhost:8000/quad"
    }
    post_link: "http:localhost:8000/Hey-ChatGPT-Automate-These-Tasks-Using-Python"
    title: "Hey ChatGPT, Automate These Tasks Using Python",
    category: "Data Science",
    slug: "Hey-ChatGPT-Automate-These-Tasks-Using-Python",
    desc: "Hey ChatGPT, Automate These Tasks Using Python"
    content: "all",
    likes: [
        username: 
            "khadijat", "quadri", "aisha"
        ]
    comments:[
        {
            username: "quadri",
            comment: "my comment"
        }
        {
            username: "faruq",
            comment: "good boy"
        }
    ]
    created_at: "2022:12:09",
    updated_at: "2022:12:30"
 }


build model queryset to get objects by category
---->Get by category and order them by most recent
---->Get all blog post and order them by timecreated

build like unlike link
----> api/{post__title}/like/

on post model
  --> like will be charcter field

  while on serializer class it will be method field


  if is_like is true 
  ===> by default user is not in the post user like
  ===> add user to list of post likes 
  ===> after been added to it user can also set it to false and removing it from the post