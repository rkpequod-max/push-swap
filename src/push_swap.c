/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void            ft_is_ordered(t_pile *p1, t_pile *p2)
{
        if (ordered(p1, 1))
        {
                free_pile(&p1);
                free_pile(&p2);
                exit(EXIT_SUCCESS);
        }
}

int                     call_alg(t_pile *p1, t_pile *p2, int k)
{

        ft_is_ordered(p1, p2);
        if (pile_len(p1) > 5)
                cost_sort(&p1, &p2, k);
        else if (pile_len(p1) >= 3)
                mini_solve(&p1, &p2, k);
        else if (pile_len(p1) == 2 && p1->x > p1->next->x)
                sab(&p1, "sa\n", k);
        free_pile(&p1);
        free_pile(&p2);
        return (0);
}

int                     ft_onearg(char **nbs, int i)
{
        if (!nbs)
                return (0);
        while (nbs[i])
                ++i;
        return (i);
}

void            ft_start(int ac, char **av)
{
        if (ac <= 1 || ((ac == 2) && !ft_strcmp(av[1], "-v")))
                exit(EXIT_SUCCESS);
}

int                     main(int ac, char **av)
{
        t_pile  *p1;
        int             i;
        int             k;
        char    **nbs;

        ft_start(ac, av);
        p1 = NULL;
        i = 0;
        k = ft_strcmp(av[1], "-v");
        if (k == 0 && av++)
                ac--;
        nbs = &av[1 + (ft_strcmp(av[1], "-v") == 0)];
        if (ac == 2)
        {
                nbs = ft_strsplit(av[1], ' ');
                i = ft_onearg(nbs, i);
                if (!i)
                        return (free_split(nbs));
                ac = i + 1;
        }
        if (!valid_input(ac - 1, nbs) || !pile_init(&p1, nbs, ac - 1))
                return (-7 + write(2, "Error\n", 6) + ((i) ? free_split(nbs) : 0));
        if (i && nbs)
                free_split(nbs);
        return (call_alg(p1, NULL, k));
}
