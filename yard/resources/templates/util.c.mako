
<%def name="functionHeader(fnData, lastChar=';')">
    <%
      retType   = fnData['returnType']
      fnName    = fnData['decoratedName']
      paramList = ['{} {}'.format(x['type'], x['name']) for x in fnData['parameters']]
    %>
    ${retType} ${fnName} (${ ', '.join(paramList) })${lastChar}
</%def>
