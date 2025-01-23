import React, { useMemo } from "react";
import { BiSortAlt2, BiSortDown, BiSortUp } from "react-icons/bi";
import { useSortBy, useTable } from "react-table";
import { useEffect } from "react";
import { useState } from "react";
import axios from "axios";

export default function Sortable({ b }) {

  const [data , setBooks] = useState([]);

  useEffect(() => {
    const fetchAllBooks = async () => {
      try {
        const res = await axios.get("http://localhost:5000/" + b);
        setBooks(res.data);
      } catch (err) {
        console.log(err);
      }
    };
    fetchAllBooks();
  }, [b]);

  // const data = useMemo(() => peopls, []);
  // console.log(data);
  
  const columns = useMemo(() => [
    // {
    //   Header: "ID",
    //   // user['id']
    //   accessor: "id",
    //   // отключаем сортировку
    //   disableSortBy: true
    // },
    {
      Header: "Имя",
      accessor: "name"
    },
    {
      Header: "Рейтинг",
      accessor: "reiting"
    },
  ], []);

  // создаем экземпляр таблицы
  const {
    // эти штуки являются обязательными
    getTableProps,
    getTableBodyProps,
    // о том, почему мы используем группы заголовков, а не сами заголовки, мы поговорим в следующем разделе
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data }, useSortBy);
  
  return (
    <table {...getTableProps()}>
      <thead>
        {headerGroups.map((hG) => (
          <tr key={"row-header"} {...hG.getHeaderGroupProps()}>
            {hG.headers.map((col) => (
              <th {...col.getHeaderProps(col.getSortByToggleProps())}>
                {col.render("Header")}{" "}
                {/* если колонка является сортируемой, рендерим рядом с заголовком соответствующую иконку в зависимости от того, включена ли сортировка, а также от порядка сортировки */}
                {col.canSort && (
                  <span>
                    {col.isSorted ? (
                      col.isSortedDesc ? (
                        <BiSortUp />
                      ) : (
                        <BiSortDown />
                      )
                    ) : (
                      <BiSortAlt2 />
                    )}
                  </span>
                )}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map((row) => {
          prepareRow(row);

          return (
            <tr {...row.getRowProps()}>
              {row.cells.map((cell) => {
                return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

// export const fetchPeopls = async () => {
//     try {
//       const res = await axios.get("http://localhost:5000/");
//       console.log()
//       // console.log(this.peopls);
//       // console.log(res.data);
//       // console.log(this.props.items);
//     } catch(err) {
//       console.log(err);
//     }
//   }