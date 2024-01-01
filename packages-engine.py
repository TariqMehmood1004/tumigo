class TumigoInterpreter:
    def __init__(self):
        self.variables = {}

    def execute(self, code):
        lines = code.split('\n')
        for line in lines:
            if line.strip().startswith("%"):
                # Ignore single-line comments
                continue
            elif line.strip().startswith("%%"):
                # Ignore multi-line comments until the closing %%
                continue
            elif line.strip().endswith("%%"):
                # Ignore the remaining part of the multi-line comment
                continue
            elif line.startswith("ptr"):
                self.handle_ptr(line)
            elif line.startswith("import_tumigo"):
                self.import_tumigo()
            elif "=" in line:
                self.assign_variable(line)
            elif line.startswith("if"):
                self.handle_if_statement(line)

    def handle_ptr(self, line):
        start_index = line.find('ptr(') + 4
        end_index = line.find(')')
        if start_index != -1 and end_index != -1:
            value_str = line[start_index:end_index].strip()
            if value_str.startswith('"') and value_str.endswith('"'):
                # Handle string interpolation
                interpolated_str = self.interpolate_string(value_str[1:-1])
                print(interpolated_str)
            elif ',' in value_str:
                # Handle case: ptr("Message: ", variable)
                message, variable_name = map(str.strip, value_str.split(',', 1))
                variable_value = self.variables.get(variable_name, None)
                print(f"{message} {variable_value}")
            else:
                variable_name = value_str
                variable_value = self.variables.get(variable_name, None)
                print(variable_value)

    def interpolate_string(self, value):
        # Interpolate expressions within the string
        parts = value.split('{')
        interpolated_str = parts[0]
        for part in parts[1:]:
            expr, remaining = part.split('}', 1)
            variable_value = str(eval(expr, {}, self.variables))
            interpolated_str += variable_value + remaining
        return interpolated_str

    def assign_variable(self, line):
        parts = line.split("=")
        if len(parts) == 2:
            variable_name = parts[0].strip()
            variable_value = eval(parts[1].strip(), {}, self.variables)
            self.variables[variable_name] = variable_value

    def import_tumigo(self):
        print("TumigoInterpreter imported!")

    def handle_if_statement(self, line):
        condition = line[2:].strip()
        if self.evaluate_condition(condition):
            self.in_if_block = True
        else:
            self.in_if_block = False

    def evaluate_condition(self, condition):
        parts = condition.split()
        variable_name = parts[0]
        operator = parts[1]
        value_str = parts[2]
        variable_value = self.variables.get(variable_name, None)
        value = eval(value_str, {}, self.variables)


        if operator == "==":
            return variable_value == value
        elif operator == "!=":
            return variable_value != value
        elif operator == "<":
            return variable_value < value
        elif operator == ">":
            return variable_value > value
        elif operator == "<=":
            return variable_value <= value
        elif operator == ">=":
            return variable_value >= value

        return False

def run_tumigo_file(file_path):
    with open(file_path, 'r') as file:
        tumigo_code = file.read()
        interpreter = TumigoInterpreter()
        interpreter.execute(tumigo_code)

# Example usage with import function and Tumigo types
tumigo_file_path = ".tumigo/main.tm"
run_tumigo_file(tumigo_file_path)
