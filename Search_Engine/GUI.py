import search_engine_best
import PySimpleGUI as sg


class GUI:
    the_searcher = search_engine_best.SearchEngine()
    file_list_column = [
        [
            sg.Text("Query: "),
            sg.In(size=(55, 1), enable_events=True, key="query"),
            sg.Button(button_text="SEARCH"),
            sg.Text("Number of results: "),
            sg.Combo([5, 10, 50, 'all'], enable_events=True, key='combo'),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(62, 40), key="tweets"
            )
        ],
    ]

    layout = [
        [
            sg.Column(file_list_column),
        ]
    ]

    window = sg.Window("More Impressive Than Google", layout)
    k = None
    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "SEARCH":
            try:
                k = int(values['combo'])
            except:
                k = None
            n_rel, relevant_docs = the_searcher.search(values['query'], k)
            window['tweets'].update(relevant_docs)
