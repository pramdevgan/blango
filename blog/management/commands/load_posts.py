import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from blog.models import Post, Tag, Comment # Make sure to import from your app

class Command(BaseCommand):
    help = 'Loads posts from a JSON file into the database'

    def handle(self, *args, **options):
        # Get the custom User model
        User = get_user_model()
        
        # Open and load the JSON file
        with open('posts.json', 'r') as f:
            posts_data = json.load(f)

        for post_data in posts_data:
            # Get or create the user
            user, created = User.objects.get_or_create(username=post_data['author'])
            if created:
                self.stdout.write(self.style.SUCCESS(f'User "{user.username}" was created.'))

            # Create the post object, using get_or_create to avoid duplicates
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'author': user,
                    'slug': post_data['slug'],
                    'summary': post_data['summary'],
                    'content': post_data['content']
                }
            )

            if not created:
                self.stdout.write(self.style.WARNING(f'Post "{post.title}" already exists. Skipping.'))
                continue

            # Add tags (ManyToManyField)
            for tag_value in post_data.get('tags', []):
                tag, _ = Tag.objects.get_or_create(value=tag_value)
                post.tags.add(tag)
            
            # Add comments (GenericRelation)
            for comment_data in post_data.get('comments', []):
                comment_creator, _ = User.objects.get_or_create(username=comment_data['creator'])
                Comment.objects.create(
                    creator=comment_creator,
                    content=comment_data['content'],
                    content_object=post # This links the comment to the post
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully created post "{post.title}"'))
