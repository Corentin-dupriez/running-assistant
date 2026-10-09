{% macro extract_from_date(column_name, pos) %}
  (string_split_regex(
                string_split_regex({{ column_name }}, ', ')[1],
                ' '
            )[{{ pos }}])
{% endmacro %}

