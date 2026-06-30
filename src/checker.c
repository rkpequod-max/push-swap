/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int		three_cmp(char *cm, char *str1, char *str2, char *str3)
{
	return ((ft_strcmp(cm, str1) == 0 || ft_strcmp(cm, str2) == 0)
			|| ft_strcmp(cm, str3) == 0);
}

int		is_cmd(t_pile **p1, t_pile **p2, char *cm, int ret)
{
	if (three_cmp(cm, "sa", "sb", "ss"))
	{
		if (ft_strcmp(cm, "sa") == 0 || ft_strcmp(cm, "ss") == 0)
			ret += sab(p1, "", 1);
		if (ft_strcmp(cm, "sb") == 0 || ft_strcmp(cm, "ss") == 0)
			ret += sab(p2, "", 1);
	}
	else if (three_cmp(cm, "ra", "rb", "rr"))
	{
		if (ft_strcmp(cm, "ra") == 0 || ft_strcmp(cm, "rr") == 0)
			ret += rab(p1, "", 1);
		if (ft_strcmp(cm, "rb") == 0 || ft_strcmp(cm, "rr") == 0)
			ret += rab(p2, "", 1);
	}
	else if (three_cmp(cm, "rra", "rrb", "rrr"))
	{
		if (ft_strcmp(cm, "rra") == 0 || ft_strcmp(cm, "rrr") == 0)
			ret += rrab(p1, "", 1);
		if (ft_strcmp(cm, "rrb") == 0 || ft_strcmp(cm, "rrr") == 0)
			ret += rrab(p2, "", 1);
	}
	else if (ft_strcmp(cm, "pa") == 0 || ft_strcmp(cm, "pb") == 0)
		ret += ((ft_strcmp(cm, "pb") == 0) ? pab(p1, p2, "", 1)
		: pab(p2, p1, "", 1));
	return (ret);
}

int		read_cmds(t_pile *p1, t_pile *p2)
{
	char		*line;
	static char	*pitcher;

	pitcher = NULL;
	while (get_next_line(0, &line, &pitcher) == 1)
	{
		if (!is_cmd(&p1, &p2, line, 0))
		{
			free_pile(&p1);
			free_pile(&p2);
			free(line);
			free(pitcher);
			ft_putendl("Error");
			return (0);
		}
		free(line);
	}
	if (line)
		free(line);
	ft_putendl((ordered(p1, 1) && !p2) ? "OK" : "KO");
	free_pile(&p1);
	free_pile(&p2);
	return (1);
}

int		main(int ac, char **av)
{
	t_pile	*p1;
	int		i;
	char	**n;

	if (ac > 1)
	{
		p1 = NULL;
		i = 0;
		n = &av[1];
		if (ac == 2)
		{
			n = ft_strsplit(av[1], ' ');
			while (n[i])
				++i;
			if (!i)
				return (free_split(n));
			ac = i + 1;
		}
		if (!valid_input(ac - 1, n) || !pile_init(&p1, n, ac - 1))
			return (-7 + write(2, "Error\n", 6) + ((i) ? free_split(n) : 0));
		(i) ? free_split(n) : 1;
		read_cmds(p1, NULL);
	}
	return (0);
}
