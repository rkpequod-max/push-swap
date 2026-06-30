/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   valid_input.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int		is_num(char *str)
{
	int i;

	i = 0;
	if (str[i])
	{
		if (str[i] == '-')
			i++;
		while (str[i])
		{
			if (!ft_isdigit(str[i++]))
				return (0);
		}
		return (1);
	}
	return (0);
}

int		is_dup(int ac, char **strs)
{
	int i;

	i = 1;
	while (i < ac)
		if (ft_strcmp(strs[0], strs[i++]) == 0)
			return (1);
	return (0);
}

int		duplicates(int ac, char **strs)
{
	int i;

	i = 0;
	while (i + 1 < ac)
	{
		if (is_dup(ac - i, &strs[i]))
			return (0);
		i++;
	}
	return (1);
}

int		valid_input(int ac, char **strs)
{
	int i;

	i = 0;
	while (i < ac)
		if (!is_num(strs[i++]))
			return (0);
	return (duplicates(ac, strs));
}
