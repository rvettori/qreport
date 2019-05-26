import unittest
from qreport import Report

class QReportTest(unittest.TestCase):
    """ How i would like to use:

        create table todos (
            id inter primary key autoincrement,
            title text not null,
            description text,
            created_at datetime default datetime(timestamp, 'localtime'),
            done integer default 0
        );

        report = Report()

        report.set_sql('select * from todos')

        report.set_title('Lista de tarefas')

        report.set_condition(created_at__gte, '2018-01-01')

        report.set_filters([title, created_at, done])

        report.set_columns([title, created_at, done])

        report.display_as('title', 'Titulo')
        report.display_as('created_at', 'Data')
        report.display_as('done', 'Finalizado?')

        report.calback_column('title', lambda value, row: '<b></b>')

        report.set_field_type('field', 'type', options={})

        return report.render()
    """
    def setUp(self):
        self.report = Report()

    def test_set_title(self):
        title = 'My Report'
        self.assertIsInstance(self.report.set_title(title), Report)
        self.assertEqual(title, self.report._title)

    def test_set_sql(self,):
        sql = 'select * from todos'
        self.assertIsInstance(self.report.set_sql(sql), Report)
        self.assertEqual(sql, self.report._sql)

    def test_set_condition(self):
        cond1 = ('title__cont', 'todo')
        self.assertIsInstance(self.report.set_condition(*cond1), Report)
        self.assertEqual(self.report._conditions, {'title__cont': 'todo'})


    def test_set_filters(self):
        filters = ['title__cont', ['created_at__gte', 'done__eq']]
        self.assertIsInstance(self.report.set_filters(filters), Report)
        self.assertEqual(len(self.report._filters), len(filters))
        self.assertEqual(self.report._filters, [['title__cont'], ['created_at__gte', 'done__eq']])


    def test_set_columns(self):
        cols = ['title', 'created_at', 'done']
        self.assertIsInstance(self.report.set_columns(cols), Report)
        self.assertEqual(len(self.report._columns), len(cols))

    def test_display_as(self):
        self.report.display_as('done', 'Feito')
        self.assertIsInstance(self.report.display_as('title', 'Titulo'), Report)
        self.assertEqual(self.report._display_as, {'title': 'Titulo', 'done': 'Feito'})

    def test_set_params(self):
        params = {
            'q': {'title__cont': 'Fazer'}
        }
        self.assertIsInstance(self.report.set_params(params), Report)
        self.assertEqual(self.report._params, params)

    def test_minimum_to_render(self):
        self.skipTest('Need continue')

        title = 'The Task List'
        self.report.set_title(title)
        self.report.set_columns(['title', 'done'])
        self.report.set_sql('select * from tasks')

        output = self.report.render()
        self.assertIn(title , output)

    def test_callback_column(self):
        def fn(value, row):
            return '<b>{}<b>'.format(value)

        instance = self.report.callback_column('title', fn)
        self.assertIsInstance(instance, Report)
        self.assertIs(fn, self.report._callback_columns['title'])

    def test_callback_footer(self):
        def fn(template, data):
            template = "<tr><th>{title}</th></tr>"
            row = {'title': 'my title in footer'}
            return (template, row)

        instance = self.report.callback_footer(fn)
        self.assertIsInstance(instance, Report)
        self.assertIs(fn, self.report._callback_footer)

    def test_set_field_type(self):
        instance = self.report.set_field_type('string', Report.FieldType.STRING)
        instance.set_field_type('inteiro', Report.FieldType.INT, format='0')
        instance.set_field_type('decimal', Report.FieldType.NUMERIC, format='0.00')
        instance.set_field_type('dropdown', Report.FieldType.DROPDOWN, *['a', 'b', 'c'])

        with self.subTest():
            self.assertIsInstance(instance, Report)
        with self.subTest():
            self.assertEqual(instance._field_types['string'], (Report.FieldType.STRING.value, {}))
        with self.subTest():
            self.assertEqual(instance._field_types['inteiro'], (Report.FieldType.INT.value, {'format':'0'}))
        with self.subTest():
            self.assertEqual(instance._field_types['decimal'], (Report.FieldType.NUMERIC.value, {'format':'0.00'}))
        with self.subTest():
            self.assertEqual(
                instance._field_types['dropdown'], (Report.FieldType.DROPDOWN.value, {'a': 'a', 'b': 'b', 'c': 'c'}))

        for it in instance._field_types.items():
            with self.subTest(): self.assertIs(type(it[0]), str)
            with self.subTest(): self.assertIs(type(it[1]), tuple)

    def test_query(self):
        result = self.report.query("select 123 as test ")
        self.assertEqual([{"test": 123}], result)

if __name__ == '__main__':
    unittest.main()
