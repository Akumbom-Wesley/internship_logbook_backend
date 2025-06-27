from django.core.management.base import BaseCommand
from apps.evaluations.models import EvaluationTemplate
from apps. evaluation_category_subfields.models import EvaluationSubfieldTemplate

class Command(BaseCommand):
    help = 'Populate evaluation templates with hardcoded categories and subfields'

    def handle(self, *args, **options):
        # Clear existing templates
        EvaluationTemplate.objects.all().delete()

        templates = [
            {
                'name': 'QUALITY OF WORK',
                'order': 1,
                'subfields': [
                    'Competency in performing assigned tasks',
                    'Respect of established standards',
                    'Respect of time allowed (deadline)',
                    'Respect of organization and engagement'
                ]
            },
            {
                'name': 'JOB KNOWLEDGE/TECHNICAL SKILLS',
                'order': 2,
                'subfields': [
                    'Demonstration of skills required to perform assigned tasks',
                    'Ability to use tools, materials and equipment effectively',
                    'Ability to use computer and related technologies effectively',
                    'Respect of established standard and operating procedure (i.e. ethics and safety protocols)'
                ]
            },
            {
                'name': 'COMMUNICATION & INTERPERSONAL SKILLS',
                'order': 3,
                'subfields': [
                    'Ability to communicate effectively',
                    'Ability to listen and understand others (i.e. colleagues, customers, partners and superiors)',
                    'Ability to work in a team to perform tasks effectively',
                    'Demonstration of mutual respect towards colleagues'
                ]
            },
            {
                'name': 'INITIATIVE/LEADERSHIP QUALITIES',
                'order': 4,
                'subfields': [
                    'Demonstration of commitment to the job',
                    'Initiative and motivation',
                    'Ability to think analytically',
                    'Ability to generate creative solutions to problems'
                ]
            },
            {
                'name': 'PERSONAL DEVELOPMENT/LEARNING',
                'order': 5,
                'subfields': [
                    'Ability to adapt to changing dynamics in the working environment',
                    'Disposition to learn new skills and knowledge',
                    'Ability to receive feedback',
                    'Endeavor to pursue opportunities for professional growth'
                ]
            }
        ]

        for template_data in templates:
            template = EvaluationTemplate.objects.create(
                name=template_data['name'],
                order=template_data['order']
            )

            for i, subfield_name in enumerate(template_data['subfields'], 1):
                EvaluationSubfieldTemplate.objects.create(
                    category=template,
                    name=subfield_name,
                    order=i
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated evaluation templates'))
